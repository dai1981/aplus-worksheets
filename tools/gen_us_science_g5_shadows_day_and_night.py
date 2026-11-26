# -*- coding: utf-8 -*-
"""
US Grade 5 Science: Shadows, Day and Night (5-ESS1-2)
  python tools/gen_us_science_g5_shadows_day_and_night.py
Earth spins once every 24 hours, so the sun seems to rise in the east, cross the sky and set in the west.
Shadows point away from the sun: long and toward the west in the morning, shortest around midday
(pointing north in the United States), long and toward the east in the evening.
Data: tables and bar graphs of shadow length during a day, and hours of daylight during a year.
Wrong answers come from real mistakes: "the sun moves around Earth each day", "shadows point toward
the sun", "the shadow is longest at noon", "day and night happen because the sun turns off".
"""
import math
from sci_common import Unit, item, bank, lesson, make, fig, figure, table, bar_chart, svg_wrap, text, line, rect, sun, People, INK, SKY

U = Unit(50112)
R = U.R
P = People(R)
OBJS = ["flagpole", "fence post", "meter stick", "lamp post", "tetherball pole", "mailbox post"]
HOURS = ["8 a.m.", "9 a.m.", "10 a.m.", "11 a.m.", "12 p.m.", "1 p.m.", "2 p.m.", "3 p.m.", "4 p.m."]
DAYLEN = [("Jan", 9.5), ("Feb", 10.6), ("Mar", 12.0), ("Apr", 13.3), ("May", 14.5), ("Jun", 15.2), ("Jul", 14.9), ("Aug", 13.8),
          ("Sep", 12.4), ("Oct", 11.0), ("Nov", 9.8), ("Dec", 9.2)]


def stick(side, height, show_shadow=True):
    """side: 'E' sun on the left (east) or 'W' on the right (west); height 1 low .. 3 high."""
    W, H = 360, 170
    gy, sx = 140, 180
    s = [rect(0, 0, W, gy, SKY, "none", 0), rect(0, gy, W, H - gy, "#d9c8a9", "none", 0), line(0, gy, W, gy, INK, 2),
         text(14, gy + 22, "EAST", 12, "start"), text(W - 14, gy + 22, "WEST", 12, "end")]
    ang = {1: 18, 2: 38, 3: 62}[height]
    d = -1 if side == "E" else 1
    sxp = sx + d * 150 * math.cos(math.radians(ang))
    syp = gy - 150 * math.sin(math.radians(ang))
    s.append(sun(sxp, max(24, syp), 14))
    s.append(line(sx, gy, sx, gy - 50, "#6b4a2b", 5))
    if show_shadow:
        L = min(160, 50 / math.tan(math.radians(ang)))
        s.append("<polygon points='%.1f,%d %.1f,%d %.1f,%d' fill='#555555' opacity='0.55'/>" % (sx, gy - 2, sx - d * L, gy - 2, sx - d * L, gy + 3))
        s.append(line(sx, gy + 1, sx - d * L, gy + 1, "#444444", 5))
    return svg_wrap(W, H, "".join(s), "stick in the sun with its shadow")


# ------------------------------------------------------------ makers
def g_dir():
    side = R.choice(["E", "W"])
    h = R.choice([1, 2])
    ob = R.choice(OBJS)
    q = fig(stick(side, h, False)) + "The sun is %s in the %s sky, as shown. Which way does the %s's shadow point?" % ("low" if h == 1 else "partway up", "eastern" if side == "E" else "western", ob)
    a = "toward the west" if side == "E" else "toward the east"
    return item(q, a, ["toward the " + ("east" if side == "E" else "west"), "straight up", "There is no shadow."],
                "A shadow points away from the sun. The sun is in the %s, so the shadow points %s." % ("east" if side == "E" else "west", a.replace("toward the ", "")))


def g_time():
    side = R.choice(["E", "W"])
    h = R.choice([1, 2])
    ob = R.choice(OBJS)
    q = fig(stick(side, h)) + "The picture shows a %s and its shadow on a sunny day. About what time of day could it be?" % ob
    if side == "E":
        a = R.choice(["8 a.m.", "9 a.m."]) if h == 1 else "10 a.m."
        w = ["12 p.m.", "4 p.m." if a != "4 p.m." else "6 p.m.", "6 p.m."]
        why = "The sun is in the east and the shadow points west, so it is morning."
    else:
        a = R.choice(["5 p.m.", "6 p.m."]) if h == 1 else "3 p.m."
        w = ["12 p.m.", "8 a.m.", "10 a.m."]
        why = "The sun is in the west and the shadow points east, so it is afternoon or evening."
    w = [x for x in w if x != a][:3]
    if len(set(w)) < 3:
        w = ["12 p.m.", "8 a.m." if side == "W" else "5 p.m.", "midnight"]
    return item(q, a, w, why)


def shadow_data():
    noon = R.choice([4, 5])                  # index of the shortest shadow: 12 p.m. or 1 p.m.
    mn = R.randint(30, 60)
    vals = [mn + int(round(9 * (i - noon) ** 2 + R.randint(0, 3))) for i in range(len(HOURS))]
    vals[noon] = mn
    return vals, noon


def g_shadow_table():
    vals, noon = shadow_data()
    pick = list(range(0, 9, 2)) if R.random() < 0.5 else [0, 2, 4, 5, 6, 8]
    if noon not in pick:
        pick = sorted(set(pick + [noon]))
    rows = [[HOURS[i], "%d cm" % vals[i]] for i in pick]
    ask = R.choice(["short", "long", "pattern"])
    tab = table(["Time", "Shadow length"], rows)
    p = P.next()
    if ask == "short":
        return item(tab + "%s measured the shadow of a meter stick during one day. At which time was the shadow shortest?" % p[0], HOURS[noon],
                    [HOURS[i] for i in pick if i != noon][:3] if len(pick) > 3 else ["8 a.m.", "4 p.m.", "10 a.m."],
                    "The shortest shadow (%d cm) was at %s, when the sun was highest in the sky." % (vals[noon], HOURS[noon]))
    if ask == "long":
        i = max(pick, key=lambda k: vals[k])
        return item(tab + "%s measured the shadow of a meter stick during one day. When was the sun lowest in the sky?" % p[0], HOURS[i],
                    [HOURS[k] for k in pick if k != i][:3], "The longest shadow (%d cm) means the sun was lowest." % vals[i])
    return item(tab + "%s measured the shadow of a meter stick during one day. Which pattern does the data show?" % p[0],
                "The shadow got shorter until about midday and then longer.", ["The shadow got longer all day.", "The shadow got shorter all day.", "The shadow stayed the same length."],
                "From %s (%d cm) it shrank to %d cm at %s, then grew again." % (HOURS[pick[0]], vals[pick[0]], vals[noon], HOURS[noon]))


def g_shadow_graph():
    vals, noon = shadow_data()
    ch = bar_chart([h.replace(" a.m.", "a").replace(" p.m.", "p") for h in HOURS], vals, "cm", "bar graph of shadow length during a day", ymax=(max(vals) // 50 + 1) * 50, step=50, col="#666666")
    i, j = R.sample(range(9), 2)
    if vals[i] == vals[j]:
        return None
    return item(fig(ch) + "The graph shows the length of a pole's shadow (a = a.m., p = p.m.). How much longer was the shadow at %s than at %s?" % (HOURS[i] if vals[i] > vals[j] else HOURS[j], HOURS[j] if vals[i] > vals[j] else HOURS[i]),
                "%d cm" % abs(vals[i] - vals[j]), ["%d cm" % max(vals[i], vals[j]), "%d cm" % (vals[i] + vals[j]), "%d cm" % (abs(vals[i] - vals[j]) + 10)],
                "%d − %d = %d cm." % (max(vals[i], vals[j]), min(vals[i], vals[j]), abs(vals[i] - vals[j])))


def g_daylen():
    pick = sorted(R.sample(range(12), 5))
    rows = [[DAYLEN[i][0], "%.1f hours" % DAYLEN[i][1]] for i in pick]
    ask = R.choice(["most", "least"])
    k = max(pick, key=lambda i: DAYLEN[i][1]) if ask == "most" else min(pick, key=lambda i: DAYLEN[i][1])
    return item(table(["Month (Chicago)", "Hours of daylight"], rows) + "In which of these months are the days %s?" % ("longest" if ask == "most" else "shortest"),
                DAYLEN[k][0], [DAYLEN[i][0] for i in pick if i != k][:3],
                "%s has %.1f hours of daylight. Days are longest near June and shortest near December in the United States." % (DAYLEN[k][0], DAYLEN[k][1]))


B1 = bank([
    ("What causes day and night?", "Earth spinning (rotating) on its axis", ["the sun moving around Earth", "the moon blocking the sun", "clouds covering the sun at night"],
     "As Earth spins, your side faces the sun (day) and then faces away (night)."),
    ("How long does it take Earth to spin around once?", "about 24 hours", ["about 1 hour", "about 7 days", "about 365 days"],
     "One full rotation is one day: about 24 hours."),
    ("Where does the sun appear to rise?", "in the east", ["in the west", "in the north", "straight overhead"],
     "Earth spins toward the east, so the sun appears in the east first."),
    ("Where does the sun appear to set?", "in the west", ["in the east", "in the south", "under your feet at noon"],
     "The sun seems to move across the sky from east to west."),
    ("Why does the sun seem to move across the sky?", "Earth is spinning, not the sun moving around us.", ["The sun circles Earth every day.", "Wind pushes the sun.", "Clouds carry the sun."],
     "It is like riding a merry-go-round: the world seems to move past you."),
    ("Which way does a shadow point?", "away from the light source", ["toward the light source", "always north", "always down the hill"],
     "An object blocks the light, so the dark shadow is on the side away from the sun."),
    ("When is your shadow shortest on a sunny day?", "around midday, when the sun is highest", ["early in the morning", "late in the evening", "at sunrise"],
     "The higher the sun, the shorter the shadow."),
    ("When are shadows longest?", "early morning and late afternoon, when the sun is low", ["at noon", "when the sun is highest", "they are always the same"],
     "A low sun makes long shadows."),
    ("In the United States, which way does a shadow point at noon?", "north", ["south", "east", "west"],
     "At noon the sun is in the southern part of the sky, so shadows point north."),
    ("When it is daytime in the United States, it is nighttime in", "places on the other side of Earth, like China", ["every place on Earth", "Canada", "Mexico"],
     "Only the half of Earth facing the sun has day."),
])
B5 = bank([
    ("Ava traces her shadow at 9 a.m. and 3 p.m. How do the two shadows compare?", "They point in opposite directions (west, then east).", ["They point the same way.", "Both point north only.", "Both are the shortest of the day."],
     "In the morning the sun is in the east; in the afternoon it is in the west."),
    ("Leo models day and night with a lamp and a globe. What should he do?", "Spin the globe in front of the lamp.", ["Move the lamp around the room quickly.", "Turn the lamp on and off.", "Put the globe in the dark."],
     "The spinning globe shows half of Earth lit (day) and half dark (night)."),
    ("Which data would best show the pattern of the sun across the sky in one day?", "the length and direction of a stick's shadow every hour", ["the temperature at midnight", "the number of clouds in a week", "the color of the sky at noon only"],
     "Shadow measurements over the day reveal the sun's path."),
    ("Why does Mia put a stick in the same spot for every shadow measurement?", "so only the time changes, not the stick or place", ["so the shadow looks bigger", "so the sun moves faster", "because sticks need to rest"],
     "Keeping everything else the same makes the measurements fair."),
    ("A sundial tells time using", "the direction of a shadow", ["the color of the sun", "the temperature", "the wind"],
     "As Earth spins, the shadow moves around the sundial like a clock hand."),
    ("In which month are noon shadows shortest in the United States?", "June", ["December", "January", "November"],
     "The noon sun is highest in summer, so shadows are shortest in June."),
])


def body():
    pics = "<div class='sn-row'>%s%s</div>" % (figure(stick("E", 1), "Morning: sun low in the east, long shadow toward the west."),
                                              figure(stick("W", 1), "Evening: sun low in the west, long shadow toward the east."))
    think = ("<p><b>Earth spins</b> on its axis once about every <b>24 hours</b>. The half facing the sun has day; the other half has night. "
             "Because Earth spins toward the east, the sun <b>appears</b> to rise in the east, cross the sky and set in the west.</p>"
             "<p>A <b>shadow</b> points away from the sun. In the morning and evening the sun is low, so shadows are long. "
             "Around midday the sun is highest, so shadows are shortest (in the United States they point north).</p>" + pics)
    ex = [("A shadow is long and points west. Is it morning or evening?", ["The shadow points away from the sun.", "So the sun is in the east."], "morning"),
          ("Shadow lengths: 9 a.m. 120 cm, 12 p.m. 40 cm, 3 p.m. 110 cm. When was the sun highest?", ["Shortest shadow = highest sun."], "12 p.m.")]
    mist = ["Thinking the sun moves around Earth each day. Earth spins.",
            "Thinking a shadow points toward the sun. It points away from it.",
            "Thinking shadows are longest at noon. They are shortest then.",
            "Thinking day and night happen everywhere at once."]
    return lesson(think, ex, mist)


def main():
    sets = U.sets([
        ("Day and night", B1 + [(g_dir, 5), (g_time, 5)]),
        ("Shadow direction", [(g_dir, 10), (g_time, 10)]),
        ("Shadow data", [(g_shadow_table, 12), (g_shadow_graph, 8)]),
        ("Patterns over a year", [(g_daylen, 10), (g_shadow_graph, 5), (g_shadow_table, 5)]),
        ("Investigations", B5 + [g_dir, g_time, g_shadow_table, g_daylen]),
    ])
    make("grade-5", "shadows-day-and-night", 12, "5-ESS1-2",
         "Represent data in graphical displays to reveal patterns of daily changes in length and direction of shadows, day and night, and the seasonal appearance of some stars in the night sky.",
         "Shadows, Day and Night",
         "Grade 5 Shadows and Day and Night Worksheets: Earth's Rotation and Shadow Data",
         "Shadows, Day and Night",
         "Free Grade 5 science worksheets on shadows, day and night (NGSS 5-ESS1-2): Earth's rotation, the sun's path from east to west, shadow length and direction, and graphs of shadow and daylight data. 100 practice questions with answers.",
         "Earth spins once a day, so the sun seems to move from east to west.",
         "Shadows point away from the sun: long in the morning and evening, shortest around midday.",
         body(),
         [("What causes day and night?", "Earth spins on its axis about once every 24 hours. The side facing the sun has day, and the side facing away has night."),
          ("Why do shadows change during the day?", "As Earth spins, the sun appears to move across the sky. A low sun makes long shadows; a high sun makes short ones. Shadows always point away from the sun."),
          ("When is a shadow shortest?", "Around midday, when the sun is highest in the sky."),
          ("Which way do shadows point in the morning?", "Toward the west, because the sun is in the east.")],
         sets)


if __name__ == "__main__":
    main()
