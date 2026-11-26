# -*- coding: utf-8 -*-
"""
US Grade 5 Science: The Sun and Other Stars (5-ESS1-1)
  python tools/gen_us_science_g5_sun_and_stars.py
The sun is a star. It looks much brighter and bigger than other stars because it is much closer
to Earth. Apparent brightness depends on distance: the same light looks dimmer from farther away.
Models: identical flashlights or lamps at different distances; identical stars in tables.
(Assessment boundary: relative distances, not sizes, of stars.)
Wrong answers come from real mistakes: "the sun is not a star", "stars are small",
"the brightest-looking star must give off the most light", "stars go away in the daytime".
"""
from sci_common import Unit, item, bank, lesson, make, fig, figure, table, svg_wrap, circle, text, line, sun, People, INK

U = Unit(50111)
R = U.R
P = People(R)
NAMES = ["Star A", "Star B", "Star C", "Star D"]


def lamps(d1, d2):
    """two identical lamps at different distances from an eye."""
    W, H = 420, 90
    s = [circle(24, 46, 10, "#ffffff", INK, 2), circle(27, 46, 4, INK, INK, 1), text(24, 80, "you", 12, weight=400)]
    mx = max(d1, d2)
    for k, (d, y) in enumerate(((d1, 28), (d2, 64))):
        x = 50 + 340 * d / float(mx)
        s.append(line(36, 46, x - 10, y, "#cccccc", 1, " stroke-dasharray='4 4'"))
        s.append(circle(x, y, 9, "#ffe58a", "#c98f00", 2) + text(x + 4, y - 13 if k == 0 else y + 24, "%d m" % d, 12))
    return svg_wrap(W, H, "".join(s), "two identical lamps at %d m and %d m" % (d1, d2))


# ------------------------------------------------------------ makers
def g_lamps():
    d1, d2 = R.sample([2, 3, 5, 8, 10, 15, 20, 30], 2)
    near = "the lamp %d m away" % min(d1, d2)
    far = "the lamp %d m away" % max(d1, d2)
    return item(fig(lamps(d1, d2)) + "Two identical lamps give off the same amount of light. One is %d m away and one is %d m away. Which looks brighter?" % (d1, d2),
                near, [far, "They look equally bright.", "You cannot see either lamp."],
                "The lamps are the same, so the closer one looks brighter. Light spreads out as it travels farther.")


def g_table_bright():
    ds = sorted(R.sample([4, 6, 9, 12, 16, 25, 40, 60, 90, 150], 4))
    names = list(NAMES)
    R.shuffle(names)
    rows = [[n, "%d light-years" % d] for n, d in zip(names, ds)]
    rows_sorted = sorted(rows)
    ask = R.choice(["brightest", "dimmest"])
    ans = names[0] if ask == "brightest" else names[-1]
    return item(table(["Star (all give off the same light)", "Distance from Earth"], rows_sorted)
                + "These four stars give off the same amount of light. Which looks the %s from Earth?" % ask, ans, [n for n in names if n != ans],
                "For identical stars, the %s one looks %s. %s is %d light-years away." % ("closest" if ask == "brightest" else "farthest", ask[:-3] + "er" if ask == "brightest" else "dimmer",
                                                                                         ans, ds[0] if ask == "brightest" else ds[-1]))


def g_times():
    a = R.choice([4, 5, 8, 10, 12, 20])
    k = R.choice([2, 3, 4, 5, 10])
    return item("Star X is %d light-years from Earth. Star Y is %d light-years away. How many times farther away is Star Y?" % (a, a * k),
                "%d times" % k, ["%d times" % (a * k - a), "%d times" % (a * k), "%d times" % (k + 1)],
                "%d ÷ %d = %d. If the stars give off the same light, Star Y looks much dimmer." % (a * k, a, k))


def g_sunvs():
    st = R.choice([("Proxima Centauri", "4.2 light-years"), ("Sirius", "8.6 light-years"), ("Alpha Centauri A", "4.4 light-years"), ("Vega", "25 light-years"),
                   ("Arcturus", "37 light-years"), ("Polaris", "about 450 light-years")])
    return item("Light from the sun takes about 8 minutes to reach Earth. Light from %s takes %s. Why does the sun look so much brighter?" % (st[0], st[1].replace("light-years", "years")),
                "The sun is much, much closer to Earth.", ["The sun is the only star that gives off light.", "%s is a planet, not a star." % st[0], "The sun is the biggest star in the universe."],
                "The sun is about 8 light-minutes away; %s is %s away. Distance makes the difference." % (st[0], st[1]))


B1 = bank([
    ("What is the sun?", "a star", ["a planet", "a moon", "a comet"],
     "The sun is a star, like the stars you see at night."),
    ("Why does the sun look much brighter than other stars?", "It is much closer to Earth than any other star.", ["It is the only star that gives off light.", "Other stars are tiny.", "Other stars are turned off in the day."],
     "The sun is about 150 million km away. The next closest star is about 270,000 times farther."),
    ("Why can't we see stars during the day?", "The sun's bright light hides their dimmer light.", ["Stars move away during the day.", "Stars only shine at night.", "Clouds always cover them."],
     "The stars are still there. Sunlight scattered in the sky outshines them."),
    ("What is a light-year?", "the distance light travels in one year", ["the time it takes to see a star", "one year on another planet", "the brightness of a star"],
     "A light-year is a distance: about 9.5 trillion kilometers."),
    ("A star looks very dim from Earth. Which could be true?", "It may be very far away.", ["It must be smaller than a house.", "It must not give off light.", "It must be a planet."],
     "Distance can make even a very bright star look dim."),
    ("Which statement about stars is true?", "Many stars are as big as or bigger than the sun.", ["All stars are smaller than Earth.", "Stars are holes in the sky.", "Stars are closer than the moon."],
     "Stars look like tiny dots only because they are so far away."),
    ("Which object in the sky is a star?", "the sun", ["the moon", "Mars", "Jupiter"],
     "The moon and planets reflect sunlight. The sun makes its own light."),
    ("Which is closest to Earth?", "the sun", ["Proxima Centauri", "Sirius", "Polaris"],
     "The sun is our closest star."),
    ("How does distance change how bright a light looks?", "The farther away, the dimmer it looks.", ["The farther away, the brighter it looks.", "Distance does not matter.", "Lights look brightest from very far away."],
     "Light spreads out as it travels, so less reaches your eyes from far away."),
    ("A streetlight looks bright up close but dim from a mile away. How is this like stars?", "Stars look dim because they are very far away.", ["Stars are streetlights.", "Stars get turned down at night.", "Stars are closer than streetlights."],
     "The same light looks dimmer from farther away."),
])
B5 = bank([
    ("Ava wants to model why the sun looks brighter than other stars. Which model is best?", "Two identical flashlights, one close and one far away", ["One flashlight that she turns on and off", "A big flashlight and a small one at the same distance", "A mirror and a ball"],
     "Identical lights at different distances show that distance changes brightness."),
    ("In Ava's model, what does the close flashlight stand for?", "the sun", ["a distant star", "Earth", "the moon"],
     "The close flashlight is like the sun, our nearby star."),
    ("Leo says the sun is not a star because it does not twinkle. What is the best reply?", "The sun is a star; other stars twinkle because their light passes through moving air from far away.", ["Leo is correct.", "Stars are planets.", "The sun is a planet that glows."],
     "The sun is close and looks like a disk, but it is a star like the others."),
    ("Sirius looks like the brightest star in the night sky. Which explanation fits?", "It gives off a lot of light and is fairly close to Earth.", ["It is the biggest star in the universe.", "It is closer than the sun.", "It is a planet."],
     "Sirius is only 8.6 light-years away and gives off more light than the sun."),
    ("Why should both flashlights in a brightness model have new batteries of the same kind?", "so they give off the same amount of light and only distance changes", ["to make them heavier", "so they are different", "so one is brighter"],
     "A fair model changes only the distance."),
    ("If the sun were moved as far away as Sirius, how would it look?", "like a faint star in the night sky", ["even brighter than now", "exactly the same", "like the moon"],
     "At that distance, the sun would be just another point of light."),
])


def body():
    think = ("<p>The <b>sun is a star</b>. It is the closest star to Earth, about 150 million kilometers away. "
             "The next closest star is more than 4 light-years away, about 270,000 times farther.</p>"
             "<p>How bright a light <b>looks</b> depends on how far away it is. The same light looks dimmer from farther away, "
             "because the light spreads out before it reaches your eyes. That is why the sun looks so much brighter and bigger than the other stars.</p>"
             + figure(lamps(3, 15), "Two identical lamps: the one 3 m away looks much brighter than the one 15 m away."))
    ex = [("Two identical stars are 10 and 50 light-years away. Which looks brighter?", ["They give off the same light.", "The closer one looks brighter."], "the one 10 light-years away"),
          ("Why can't we see stars in the daytime?", ["Stars are always shining.", "The sun's light fills the sky and hides their dim light."], "The sunlight outshines them.")]
    mist = ["Thinking the sun is not a star. It is a star that is very close.",
            "Thinking the brightest-looking star gives off the most light. Distance matters too.",
            "Thinking stars disappear in the daytime. Sunlight hides them.",
            "Thinking a light-year is a time. It is a distance."]
    return lesson(think, ex, mist)


def main():
    sets = U.sets([
        ("The sun is a star", B1 + [(g_sunvs, 6), (g_lamps, 4)]),
        ("Distance and brightness", [(g_lamps, 12), (g_table_bright, 8)]),
        ("Comparing stars", [(g_table_bright, 10), (g_times, 10)]),
        ("Evidence about the sun", [(g_sunvs, 8), (g_times, 6), (g_lamps, 6)]),
        ("Models and arguments", B5 + [g_lamps, g_table_bright, g_times, g_sunvs]),
    ])
    make("grade-5", "sun-and-stars", 11, "5-ESS1-1",
         "Support an argument that differences in the apparent brightness of the sun compared to other stars is due to their relative distances from Earth.",
         "The Sun and Other Stars",
         "Grade 5 Sun and Stars Worksheets: Why the Sun Looks Brighter, Distance and Light-Years",
         "Sun and Stars",
         "Free Grade 5 science worksheets on the sun and other stars (NGSS 5-ESS1-1): the sun is a star, distance and apparent brightness, light-years, and flashlight models. 100 practice questions with answers.",
         "The sun looks brightest because it is the closest star.",
         "The same light looks dimmer from farther away. Other stars look like faint dots only because they are so far from Earth.",
         body(),
         [("Is the sun a star?", "Yes. The sun is a star. It is the closest star to Earth."),
          ("Why does the sun look brighter than other stars?", "Because it is much closer. Light looks dimmer the farther it travels, and other stars are hundreds of thousands of times farther away."),
          ("What is a light-year?", "The distance light travels in one year, about 9.5 trillion kilometers. It measures distance, not time."),
          ("Why can't we see stars during the day?", "The stars are still shining, but the sun's bright light fills the sky and hides their dimmer light.")],
         sets)


if __name__ == "__main__":
    main()
