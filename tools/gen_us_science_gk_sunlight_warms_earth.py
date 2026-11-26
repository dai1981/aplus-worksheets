# -*- coding: utf-8 -*-
"""
US Kindergarten Science: Sunlight Warms the Earth (K-PS3-1)
  python tools/gen_us_science_gk_sunlight_warms_earth.py
Make observations to determine the effect of sunlight on Earth's surface. Sand, soil, rocks, water and slides get warmer
in the sun than in the shade; ice melts faster in the sun; reading two simple thermometers.
Very short sentences for 5-6 year olds; almost every question has a picture.
Wrong answers come from real mistakes: "shade is warmer", "the sun only makes light, not heat", "water does not warm up".
"""
from sci_common import Unit, item, bank, kid_lesson, make, fig, svg_wrap, People
from ws_common import text, INK
import sci_kids as K

U = Unit(9103)
R = U.R
P = People(R)
USED = {}


def once(key, n=1):
    USED[key] = USED.get(key, 0) + 1
    return USED[key] <= n


THINGS = [("rock", "a rock"), ("cup", "a cup of water"), ("ball", "a ball"), ("block", "a wooden block"), ("spoon", "a metal spoon"), ("ice", "an ice cube"),
          ("crayon", "a crayon"), ("apple", "an apple")]


def sunshade_svg(kind, label=True):
    s = "<rect x='0' y='0' width='360' height='150' fill='#e6f3fc'/><rect x='0' y='112' width='360' height='38' fill='#cfe7b8'/>"
    s += K.icon("sun", 40, 30, 0.6)
    s += "<path d='M60 46 L110 100' stroke='#f0b400' stroke-width='3' stroke-dasharray='6 5'/>"
    s += K.icon(kind, 110, 108, 0.55)
    s += K.icon("tree", 270, 64, 1.1) + "<ellipse cx='270' cy='122' rx='60' ry='10' fill='#7a9a6a' opacity='0.6'/>"
    s += K.icon(kind, 270, 108, 0.55)
    if label:
        s += text(110, 144, "A: sun", 13) + text(270, 144, "B: shade", 13)
    return svg_wrap(360, 150, s, "two %s: A in the sun, B in the shade of a tree" % K.name(kind))


def g_warm():
    k, nm = R.choice(THINGS)
    who = P.next()[0]
    q = R.choice(["warm", "cool", "why"])
    if not once((k, q)):
        return None
    pic = fig(sunshade_svg(k))
    if q == "warm":
        return item(pic + "%s puts %s in the sun and %s in the shade. After an hour, which is warmer?" % (who, nm, nm.replace("a ", "another ", 1).replace("an ", "another ", 1)),
                    "A, in the sun", ["B, in the shade", "They are the same.", "Neither one changes."], "Sunlight warms things.")
    if q == "cool":
        return item(pic + "Look at %s's test. Which %s stays cooler?" % (who, K.name(k)), "B, in the shade", ["A, in the sun", "They are the same.", "Both get hot."], "Shade blocks sunlight.")
    return item(pic + "Why does %s's %s in the sun get warmer?" % (who, K.name(k)), "Sunlight shines on it.", ["The tree makes it warm.", "The grass makes it warm.", "It is wet."],
                "Sunlight warms Earth's surface.")


PLACES = [("a metal slide in the sun", "hot", "a slide in the shade"), ("sand at the beach in the sun", "hot", "sand under an umbrella"),
          ("a sidewalk in the sun", "hot", "a sidewalk in the shade"), ("a puddle in the sun", "warm", "a puddle in the shade"),
          ("a car seat in the sun", "hot", "a car seat in a garage"), ("a rock in the sun", "warm", "a rock under a tree"),
          ("dark soil in the sun", "warm", "soil under a bush"), ("a pool in the sun", "warm", "a pool with a cover")]


def g_touch():
    a, feel, b = R.choice(PLACES)
    who = P.next()[0]
    t = R.random() < 0.5
    if not once((a, t)):
        return None
    if t:
        return item(fig(K.card("sun")) + "%s touches %s. How does it feel?" % (who, a), feel, ["cold", "wet", "the same as in the shade"], "The sun warmed it.")
    x, y = (a, b) if R.random() < 0.5 else (b, a)
    return item("%s touches %s and %s. Which feels warmer?" % (who, x, y), a, [b, "They feel the same.", "Neither one."], "Sunlight makes it warmer.")


def thermo(x, level, lab):
    s = "<rect x='%d' y='20' width='16' height='100' rx='8' fill='#fff' stroke='%s' stroke-width='1.6'/>" % (x - 8, INK)
    s += "<rect x='%d' y='%d' width='8' height='%d' fill='#e05a4f'/>" % (x - 4, 116 - level, level)
    s += "<circle cx='%d' cy='124' r='11' fill='#e05a4f' stroke='%s' stroke-width='1.6'/>" % (x, INK)
    s += text(x, 152, lab, 13)
    return s


def g_thermo():
    who = P.next()[0]
    hi, lo = R.randint(60, 90), R.randint(20, 45)
    place = R.choice(["sand", "soil", "water", "a rock", "a sidewalk", "a slide", "a puddle", "a brick"])
    order = R.random() < 0.5
    k = R.choice(["which", "why"])
    if not once((place, k, order)):
        return None
    s = thermo(70, hi if order else lo, "A") + thermo(170, lo if order else hi, "B")
    pic = svg_wrap(240, 160, s, "two thermometers: A is %s, B is %s" % ("high" if order else "low", "low" if order else "high"))
    sunny = "A" if order else "B"
    if k == "which":
        return item(fig(pic) + "%s measured %s in the sun and in the shade. Which thermometer was in the sun?" % (who, place), sunny, ["B" if sunny == "A" else "A", "both", "neither"],
                    "The higher red line is warmer. The sun warmed it.")
    return item(fig(pic) + "%s's thermometer %s is higher. What does that mean?" % (who, sunny), "It is warmer.", ["It is colder.", "It is wetter.", "It is darker."], "Higher line, warmer.")


def g_ice():
    who = P.next()[0]
    k = R.choice(["fast", "slow", "where"])
    if not once(k):
        return None
    pic = fig(sunshade_svg("ice"))
    if k == "fast":
        return item(pic + "%s puts ice in the sun and in the shade. Which ice melts first?" % who, "A, in the sun", ["B, in the shade", "They melt at the same time.", "Neither melts."], "Sunlight warms the ice.")
    if k == "slow":
        return item(pic + "%s wants an ice cube to last longer. Where should it go?" % who, "in the shade", ["in the sun", "on a hot sidewalk", "on a sunny window"], "Shade keeps it cooler.")
    return item(pic + "%s's ice in the sun is gone. What happened?" % who, "It melted into water.", ["It turned into a rock.", "It flew away.", "It got bigger."], "Sunlight warmed and melted it.")


TIME_OBJ = ["a rock", "the sand", "a slide", "a sidewalk", "a puddle", "a bench", "the soil", "a toy truck left outside"]


def g_time():
    ob = R.choice(TIME_OBJ)
    who = P.next()[0]
    q = R.choice(["warmer", "cooler"])
    order = R.random() < 0.5
    if not once((ob, q, order)):
        return None
    t1, t2 = ("in the early morning", "in the afternoon") if order else ("in the afternoon", "in the early morning")
    a = "in the afternoon" if q == "warmer" else "in the early morning"
    return item(fig(K.card("sun")) + "On a sunny day, %s touches %s %s and %s. When does it feel %s?" % (who, ob, t1, t2, q), a,
                ["in the early morning" if a == "in the afternoon" else "in the afternoon", "It feels the same.", "It never changes."],
                "The sun shines on it all day, so it gets warmer.")


B1 = bank([
    ("What does sunlight do to the ground?", "warms it", ["cools it", "makes it wet", "makes it dark"], "Sunlight brings warmth."),
    ("Where is it cooler on a sunny day?", "in the shade", ["in the sun", "on a sunny sidewalk", "on a metal slide in the sun"], "Shade blocks sunlight."),
    ("What makes shade?", "something blocking the sunlight, like a tree", ["more sunlight", "a puddle", "the wind"], "Shade is where light is blocked."),
    ("A slide sits in the sun all morning. How does it feel?", "hot", ["cold", "wet", "soft"], "Sunlight warmed it."),
    ("Does sunlight warm water too?", "yes", ["no, never", "only ice", "only at night"], "Pools and puddles warm up."),
    ("When is a sidewalk warmest?", "on a sunny afternoon", ["at night", "on a cloudy morning", "in the shade"], "Sunlight all day."),
    ("Why do we sit under an umbrella at the beach?", "to stay cool in the shade", ["to get warmer", "to get wet", "to find shells"], "Shade keeps you cool."),
    ("What tool tells us how warm something is?", "a thermometer", ["a ruler", "a clock", "a cup"], "It measures temperature."),
])
B5 = bank([
    ("Ava puts one toy car in the sun and one in the shade. Which is warmer later?", "the one in the sun", ["the one in the shade", "both the same", "neither"], "Sun warms."),
    ("Leo's sand in the sun is 30 degrees. Sand in the shade is 20 degrees. How much warmer is the sunny sand?", "10 degrees", ["50 degrees", "20 degrees", "3 degrees"], "30 − 20 = 10."),
    ("Mia wants to keep her water bottle cool. Where should she put it?", "in the shade", ["in the sun", "on a hot car seat", "on the sunny sidewalk"], "Shade stays cool."),
    ("Kai tests a dark rock and a dark rock under a box in the sun. Which is warmer?", "the rock out in the sun", ["the rock under the box", "both the same", "neither"], "The box blocks sunlight."),
    ("Why is the beach sand hot at noon?", "The sun has warmed it all morning.", ["The ocean heated it.", "Wind heated it.", "It is always hot."], "Sunlight warms sand."),
])


def body():
    pic = sunshade_svg("rock")
    ex = [("A rock is in the sun. Another is in the shade. Which is warmer?", ["The sun warms things."], "the rock in the sun"),
          ("Where should you put ice so it lasts?", ["Shade is cooler."], "in the shade")]
    mist = ["Thinking the shade is warmer than the sun.",
            "Thinking the sun gives light but no warmth.",
            "Thinking water does not warm up in the sun."]
    return kid_lesson(pic, "The sun warms things.",
                      ["Sun: warm.", "Shade: cooler.", "Sand, rocks and water get warm in the sun."], ex, mist)


def main():
    sets = U.sets([
        ("Sun and shade", B1 + [(g_warm, 6), (g_touch, 6)]),
        ("Which is warmer?", [(g_warm, 10), (g_touch, 6), (g_ice, 2), (g_time, 2)]),
        ("Feel the warmth", [(g_touch, 4), (g_warm, 6), (g_thermo, 6), (g_time, 4)]),
        ("Thermometers", [(g_thermo, 10), (g_time, 7), (g_ice, 1), (g_warm, 2)]),
        ("Sun scientists", B5 + [(g_thermo, 8), (g_time, 7)]),
    ])
    make("kindergarten", "sunlight-warms-earth", 3, "K-PS3-1",
         "Make observations to determine the effect of sunlight on Earth's surface.",
         "Sunlight Warms the Earth",
         "Kindergarten Sunlight Worksheets: The Sun Warms Sand, Rocks and Water",
         "Sunlight Warms Earth",
         "Free kindergarten science worksheets on sunlight (NGSS K-PS3-1): things in the sun get warmer than things in the shade, ice melting and simple thermometers. 100 picture questions with answers.",
         "The sun warms things.",
         "Things in the sun get warmer than things in the shade.",
         body(),
         [("What does sunlight do to Earth's surface?", "It warms it. Sand, soil, rocks and water get warmer in the sun."),
          ("Why is shade cooler?", "Something, like a tree or an umbrella, blocks the sunlight."),
          ("How can kids test it?", "Put two of the same thing in the sun and in the shade, then touch them or use a thermometer.")],
         sets)


if __name__ == "__main__":
    main()
