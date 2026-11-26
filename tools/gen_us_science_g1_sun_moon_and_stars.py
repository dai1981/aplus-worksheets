# -*- coding: utf-8 -*-
"""
US Grade 1 Science: Sun, Moon and Stars (1-ESS1-1)
  python tools/gen_us_science_g1_sun_moon_and_stars.py
Use observations of the sun, moon, and stars to describe patterns that can be predicted.
The sun rises in the east, is high at midday and sets in the west; stars are seen at night; the moon can be seen at night
and sometimes in the day, and its shape changes in a pattern that repeats about every month.
Very short sentences, many pictures.
Wrong answers come from real mistakes: "stars go away in the day", "the sun sets in the east", "the moon is only out at night".
"""
import math
from sci_common import Unit, item, bank, kid_lesson, make, fig, svg_wrap, People
from ws_common import text, INK
import sci_kids as K

U = Unit(10108)
R = U.R
P = People(R)
USED = {}


def once(key, n=1):
    USED[key] = USED.get(key, 0) + 1
    return USED[key] <= n


POS = {"morning": (70, 104), "midday": (200, 36), "evening": (330, 104)}


def sky_svg(when, labels=True):
    night = when == "night"
    s = "<rect x='0' y='0' width='400' height='150' fill='%s'/>" % ("#1f2a4a" if night else "#dff1fb")
    s += "<path d='M0 130 Q200 110 400 130 L400 170 L0 170 Z' fill='#9fcf7a'/>"
    if night:
        for x, y in [(40, 30), (90, 60), (150, 25), (260, 40), (330, 70), (370, 25), (210, 80)]:
            s += K.icon("star", x, y, 0.25)
        s += K.icon("moon", 300, 40, 0.5)
    else:
        x, y = POS[when]
        s += "<path d='M60 128 Q200 -40 340 128' fill='none' stroke='#c9a95a' stroke-dasharray='5 5' stroke-width='1.5'/>"
        s += K.icon("sun", x, y, 0.6)
    s += K.icon("house", 200, 126, 0.5)
    if labels:
        s += text(26, 162, "east", 13) + text(374, 162, "west", 13)
    return svg_wrap(400, 170, s, "the sky at night with the moon and stars" if night else "the sky in the %s; the sun is %s" % (when, {"morning": "low in the east", "midday": "high in the sky", "evening": "low in the west"}[when]))


def g_when():
    when = R.choice(["morning", "midday", "evening", "night"])
    who = P.next()[0]
    k = R.choice(["time", "next"])
    if not once((when, k)):
        return None
    pic = fig(sky_svg(when))
    if k == "time":
        return item(pic + "%s draws the sky. What time of day is it?" % who, when if when != "midday" else "midday (noon)",
                    [x if x != "midday" else "midday (noon)" for x in ["morning", "midday", "evening", "night"] if x != when], "Look where the sun is, or if it is dark.")
    nxt = {"morning": "The sun moves higher in the sky.", "midday": "The sun moves lower toward the west.", "evening": "The sun sets and it gets dark.", "night": "The sun rises in the east."}
    return item(pic + "This is %s's picture. What will happen next?" % who, nxt[when], [nxt[x] for x in nxt if x != when], "The sun makes the same path every day.")


def g_dir():
    who = P.next()[0]
    k = R.choice(["rise", "set", "mid"])
    if not once((k, who)) or not once(k, 4):
        return None
    if k == "rise":
        return item("%s wakes up early. Where does %s see the sun rise?" % (who, who), "in the east", ["in the west", "straight overhead", "under the ground"], "The sun rises in the east.")
    if k == "set":
        return item("%s watches the sunset. Where does the sun go down?" % who, "in the west", ["in the east", "straight overhead", "in the south only"], "The sun sets in the west.")
    return item("%s eats lunch outside at noon. Where is the sun?" % who, "high in the sky", ["low in the east", "low in the west", "under the ground"], "At midday the sun is highest.")


SEE = [("the sun", "day"), ("stars", "night"), ("the moon", "both"), ("a bright full moon rising", "night"), ("many twinkling stars", "night"), ("a sunrise", "day")]


def g_see():
    th, when = R.choice(SEE)
    who = P.next()[0]
    if not once(th):
        return None
    a = {"day": "in the daytime", "night": "at night", "both": "at night, and sometimes in the daytime too"}[when]
    w = [v for k, v in {"day": "in the daytime", "night": "at night", "both": "at night, and sometimes in the daytime too"}.items() if k != when] + ["never"]
    return item("When can %s see %s?" % (who, th), a, w, {"day": "The sun lights the day.", "night": "Stars are there all the time, but the sun is too bright to see them in the day.", "both": "The moon can be seen in the day sometimes."}[when])


PHASES = ["new moon", "crescent", "half moon", "full moon"]
CYCLE = ["new moon", "crescent", "half moon", "full moon", "half moon", "crescent"]


def moon_svg(phase, x, y, r=22, waning=False):
    s = "<circle cx='%g' cy='%g' r='%g' fill='#2b3550' stroke='%s' stroke-width='1.2'/>" % (x, y, r, INK)
    if phase == "full moon":
        s += "<circle cx='%g' cy='%g' r='%g' fill='#f6e7a6'/>" % (x, y, r)
    elif phase == "half moon":
        sx = -1 if waning else 1
        s += "<path d='M%g %g A%g %g 0 0 %d %g %g Z' fill='#f6e7a6'/>" % (x, y - r, r, r, 1 if sx > 0 else 0, x, y + r)
    elif phase == "crescent":
        sx = -1 if waning else 1
        s += "<path d='M%g %g A%g %g 0 0 %d %g %g A%g %g 0 0 %d %g %g Z' fill='#f6e7a6'/>" % (
            x, y - r, r, r, 1 if sx > 0 else 0, x, y + r, r * 0.55, r, 0 if sx > 0 else 1, x, y - r)
    return s


def g_phase():
    start = R.randrange(6)
    n = R.choice([3, 4])
    ask = R.choice(["next", "before"])
    who = P.next()[0]
    if not once((start, n, ask)):
        return None
    if ask == "next":
        idx = [(start + i) % 6 for i in range(n)]
        miss = (start + n) % 6
        slots = idx + [None]
    else:
        miss = start
        idx = [(start + 1 + i) % 6 for i in range(n)]
        slots = [None] + idx
    sv = ""
    for i, j in enumerate(slots):
        x = 40 + i * 70
        if j is None:
            sv += text(x, 48, "?", 24)
        else:
            sv += moon_svg(CYCLE[j], x, 40, 22, j in (4, 5))
    pic = svg_wrap(40 + len(slots) * 70 - 10, 84, sv, "moon shapes in order, with one missing: " + ", ".join("?" if j is None else CYCLE[j] for j in slots))
    a = CYCLE[miss]
    return item(fig(pic) + "%s draws the moon every few nights. Which shape is missing?" % who, a, [p for p in PHASES if p != a], "The moon's shape changes in a pattern that repeats.")


TIMES = [("6:30 in the morning", "low in the east"), ("7:00 in the morning", "low in the east"), ("8:00 in the morning", "low in the east"),
         ("12:00 noon", "high in the sky"), ("1:00 in the afternoon", "high in the sky"), ("6:00 in the evening", "low in the west"),
         ("7:00 in the evening", "low in the west"), ("midnight", "not in the sky; it is night")]


def g_time():
    t, a = R.choice(TIMES)
    who = P.next()[0]
    if not once(t):
        return None
    opts = ["low in the east", "high in the sky", "low in the west", "not in the sky; it is night"]
    return item("It is %s on a sunny day. Where should %s look for the sun?" % (t, who), a, [o for o in opts if o != a], "Morning: east. Noon: high. Evening: west.")


def g_pick():
    kinds = ["sun", "moon", "star", "cloud"]
    R.shuffle(kinds)
    q = R.choice([("Which one makes the daytime bright?", "sun"), ("Which one changes shape in a pattern each month?", "moon"),
                  ("Which one is a tiny dot of light we see at night?", "star"), ("Which one rises in the east every morning?", "sun"),
                  ("Which one can we sometimes see in both the day and the night?", "moon"), ("Which one is NOT in space?", "cloud")])
    if not once((q[0], tuple(kinds))) or not once(q[0], 3):
        return None
    L = "ABCD"
    pic = K.row(kinds, words=["%s. %s" % (L[i], k) for i, k in enumerate(kinds)], size=90)
    a = q[1]
    return item(fig(pic) + q[0], "%s (%s)" % (L[kinds.index(a)], a), ["%s (%s)" % (L[i], k) for i, k in enumerate(kinds) if k != a], "The answer is the %s." % a)


PRED = [("The sun rose at 7:00 today. What will it do tomorrow morning?", "rise again in the east", ["rise in the west", "not rise at all", "rise at midnight"]),
        ("It is a full moon tonight. In about 2 weeks, how will the moon look?", "dark, or almost dark (new moon)", ["still full", "square", "green"]),
        ("It is dark and the stars are out. What will happen in the morning?", "The sun will rise and we will not see the stars.", ["The stars will fall.", "It will stay dark.", "The moon will go away forever."]),
        ("The sun is high at noon. What will it look like at 5:00?", "lower in the west", ["higher than at noon", "in the east", "gone forever"]),
        ("Every night this week the moon got bigger. What will it look like next?", "bigger, until it is full", ["it will disappear forever", "a square", "a star"]),
        ("Last summer the days were long. What will next summer be like?", "long days again", ["no days", "short days", "only nights"]),
        ("Today the sun set behind the big tree in the west. Where will it set tomorrow?", "in the west again", ["in the east", "in the north", "it will not set"]),
        ("It is a new moon tonight. In about 2 weeks, how will the moon look?", "full and round", ["dark again", "square", "gone forever"]),
        ("The sun is just rising. Where will it be at noon?", "high in the sky", ["low in the west", "under the ground", "in the same spot"]),
        ("The moon is a half moon and getting bigger. What comes next?", "a full moon", ["a new moon", "a square moon", "the sun"]),
        ("You saw Orion's stars in the winter sky. Where can you look for them next winter?", "in the winter sky again", ["in the summer daytime sky", "nowhere", "inside the moon"]),
        ("At night you see the Big Dipper. Tonight, where is the sun?", "on the other side of Earth, not in our sky", ["behind the moon", "in the Big Dipper", "under your bed"])]


def g_pred():
    q, a, w = R.choice(PRED)
    if not once(q):
        return None
    return item(q, a, w, "Sky patterns repeat, so we can predict them.")


def g_star():
    who = P.next()[0]
    k = R.choice(["day", "city", "same"])
    if not once((k, who)) or not once(k, 3):
        return None
    if k == "day":
        return item("Why can't %s see stars in the daytime?" % who, "The sun is so bright that it hides them.", ["Stars go away in the day.", "Stars fall down in the day.", "Stars sleep in the day."],
                    "Stars are still there.")
    if k == "city":
        return item("%s sees more stars at a farm than in a big city. Why?" % who, "City lights make the sky too bright.", ["Farms have more stars.", "Stars hate cities.", "Cities are closer to the sun."],
                    "A dark sky shows more stars.")
    return item("%s sees the Big Dipper star pattern in summer. Next summer, will it look the same?" % who, "Yes. Star patterns repeat.", ["No. It will be gone.", "No. It will be a new shape.", "No. Stars move away."],
                "Star patterns are predictable.")


B1 = bank([
    ("Where does the sun rise?", "in the east", ["in the west", "in the north", "under the house"], "Every morning, in the east."),
    ("Where does the sun set?", "in the west", ["in the east", "in the north", "in the clouds"], "Every evening, in the west."),
    ("When is the sun highest in the sky?", "at midday (noon)", ["at sunrise", "at sunset", "at midnight"], "Noon is the top."),
    ("What can you see in the sky at night?", "the moon and stars", ["only the sun", "nothing ever", "only clouds"], "Night sky."),
    ("Can you sometimes see the moon in the day?", "yes", ["no, never", "only in winter", "only on your birthday"], "The moon can be up in the day."),
    ("Does the moon's shape change?", "Yes, in a pattern each month.", ["No, it is always full.", "Yes, but with no pattern.", "Only when it rains."], "It repeats."),
    ("What is the biggest light in the day sky?", "the sun", ["the moon", "a star", "a cloud"], "The sun is a star close to us."),
    ("Will the sun rise again tomorrow?", "yes, in the east", ["no", "yes, in the west", "only on sunny days"], "It is a pattern."),
])
B5 = bank([
    ("Ava sees a full moon tonight. In about one month, what will she see?", "a full moon again", ["no moon ever again", "a square moon", "the sun at night"], "The pattern repeats."),
    ("Leo sees the sun low in the east. What time is it?", "morning", ["noon", "evening", "midnight"], "East and low = morning."),
    ("Mia draws the sun 3 times in one day: low east, high, low west. What does this show?", "The sun seems to move across the sky.", ["The sun stays still.", "The sun jumps.", "There are 3 suns."], "Same path every day."),
    ("Kai says stars only come out at night. What is true?", "Stars are always there, but the sun hides them in the day.", ["Kai is right.", "Stars are made at night.", "Stars live in the moon."], "The sun is too bright."),
    ("Zoe wants to predict when the sun will set. Which helps most?", "watching when it sets for many days", ["looking at the moon once", "counting clouds", "guessing"], "Patterns help us predict."),
])


def body():
    pic = sky_svg("morning")
    ex = [("The sun is low in the east. What time is it?", ["The sun rises in the east."], "morning"),
          ("Full moon, half moon, crescent, ... What comes next?", ["The pattern goes on."], "new moon")]
    mist = ["Thinking stars go away in the day.",
            "Thinking the sun sets in the east.",
            "Thinking the moon is only out at night."]
    return kid_lesson(pic, "The sky has patterns.",
                      ["Sun: rises east, high at noon, sets west.", "Stars: we see them at night.", "Moon: its shape changes in a pattern."], ex, mist)


def main():
    sets = U.sets([
        ("Day and night sky", B1 + [(g_when, 6), (g_see, 6)]),
        ("The sun's path", [(g_when, 2), (g_dir, 6), (g_time, 8), (g_pick, 4)]),
        ("Moon shapes", [(g_phase, 14), (g_pick, 4), (g_star, 2)]),
        ("Stars and patterns", [(g_star, 7), (g_pred, 7), (g_phase, 4), (g_pick, 2)]),
        ("Sky watchers", B5 + [(g_phase, 4), (g_pick, 3), (g_dir, 3), (g_pred, 5)]),
    ])
    make("grade-1", "sun-moon-and-stars", 8, "1-ESS1-1",
         "Use observations of the sun, moon, and stars to describe patterns that can be predicted.",
         "Sun, Moon and Stars",
         "Grade 1 Sun, Moon and Stars Worksheets: Patterns in the Sky",
         "Sun, Moon and Stars",
         "Free grade 1 science worksheets on the sun, moon and stars (NGSS 1-ESS1-1): sunrise and sunset, moon shapes and star patterns you can predict. 100 picture questions with answers.",
         "The sky has patterns.",
         "The sun rises in the east and sets in the west. The moon changes shape.",
         body(),
         [("Where does the sun rise and set?", "It rises in the east, is highest at midday and sets in the west, every day."),
          ("Why can't we see stars in the day?", "The stars are still there, but the sun is so bright that it hides them."),
          ("How does the moon change?", "Its shape changes from new to crescent, half and full, and back again, about once a month.")],
         sets)


if __name__ == "__main__":
    main()
