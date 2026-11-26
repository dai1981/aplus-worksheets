# -*- coding: utf-8 -*-
"""
US Grade 2 Science: Fast and Slow Earth Changes (2-ESS1-1)
  python tools/gen_us_science_g2_fast_and_slow_earth_changes.py
Use information from several sources to provide evidence that Earth events can occur quickly or slowly.
Fast: volcanic eruptions, earthquakes, landslides, floods (minutes, hours, days). Slow: canyons carved by rivers,
rocks wearing down, mountains wearing away, glaciers moving (hundreds to millions of years).
Wrong answers come from real mistakes: "the Grand Canyon formed in one big flood", "rocks never change", "slow means it never happens".
"""
from sci_common import Unit, item, bank, kid_lesson, make, fig, svg_wrap, arrow, People
from ws_common import text, INK
import sci_kids as K

U = Unit(20108)
R = U.R
P = People(R)
USED = {}


def once(key, n=1):
    USED[key] = USED.get(key, 0) + 1
    return USED[key] <= n


# event, fast/slow, time words
EV = [("A volcano erupts and lava covers a hill.", "fast", "hours or days"),
      ("An earthquake shakes the ground and cracks a road.", "fast", "seconds or minutes"),
      ("A landslide sends mud and rocks down a hill.", "fast", "minutes"),
      ("A flood fills a town's streets with water.", "fast", "hours or days"),
      ("A big storm wave knocks down part of a sand dune.", "fast", "hours"),
      ("A rock falls off a cliff.", "fast", "seconds"),
      ("A river carves a deep canyon.", "slow", "millions of years"),
      ("Wind and rain wear a big rock into sand.", "slow", "thousands of years"),
      ("A tall mountain wears down and gets shorter.", "slow", "millions of years"),
      ("A glacier slides down a valley and shapes it.", "slow", "thousands of years"),
      ("Ocean waves wear away a rocky cliff.", "slow", "hundreds of years"),
      ("Tree roots crack a big rock.", "slow", "many years"),
      ("Layers of mud pile up and turn into rock.", "slow", "millions of years"),
      ("A cave forms as water dissolves rock.", "slow", "thousands of years")]
SHORT = {"volc": "a volcano erupting", "An e": "an earthquake", "A la": "a landslide", "A fl": "a flood", "A bi": "a storm wave hitting a dune", "A ro": "a rock falling off a cliff",
         "A ri": "a river carving a canyon", "Wind": "a rock wearing into sand", "A ta": "a mountain wearing down", "A gl": "a glacier shaping a valley",
         "Ocea": "waves wearing away a cliff", "Tree": "roots cracking a rock", "Laye": "mud turning into rock", "A ca": "a cave forming"}


def short(e):
    return SHORT["volc" if e.startswith("A volcano") else e[:4]]


FAST_T = ["seconds or minutes", "hours or days", "minutes", "hours", "seconds"]
SLOW_T = ["millions of years", "thousands of years", "hundreds of years", "many years"]


def g_speed():
    e, sp, t = R.choice(EV)
    who = P.next()[0]
    k = R.random() < 0.55
    if not once((e, k)):
        return None
    if k:
        return item("%s reads: “%s” Is this a fast change or a slow change?" % (who, e), sp, ["slow" if sp == "fast" else "fast", "It never happens.", "It happens every day in every town."],
                    "It takes %s, so it is %s." % (t, sp))
    good = t
    bad = R.sample(SLOW_T if sp == "fast" else FAST_T, 2) + ["exactly one week"]
    return item("%s reads: “%s” How long does this usually take?" % (who, e), good, bad, "This is a %s change: %s." % (sp, t))


def g_which():
    a, b = R.sample(EV, 2)
    if a[1] == b[1]:
        return None
    who = P.next()[0]
    q = R.choice(["faster", "slower"])
    if not once((a[0], b[0], q)):
        return None
    ans = a if (a[1] == "fast") == (q == "faster") else b
    oth = b if ans is a else a
    return item("%s compares %s and %s. Which happens %s?" % (who, short(a[0]), short(b[0]), q), short(ans[0]), [short(oth[0]), "They take the same time.", "Neither one changes the land."],
                "%s takes %s; %s takes %s." % (short(ans[0])[0].upper() + short(ans[0])[1:], ans[2], short(oth[0]), oth[2]))


SOURCES = [("photos of a cliff taken 50 years apart that look almost the same", "slow", "The cliff barely changed in 50 years."),
           ("a video of mud sliding over a road in 1 minute", "fast", "It happened in 1 minute."),
           ("a book that says the canyon took millions of years to form", "slow", "Millions of years is very slow."),
           ("a news story about an earthquake that lasted 30 seconds", "fast", "It lasted only seconds."),
           ("a map of a glacier that moved a few feet each year", "slow", "A few feet a year is very slow."),
           ("a photo of a town flooded the day after a big storm", "fast", "It happened in one day."),
           ("a chart showing a beach losing a little sand each year for 100 years", "slow", "A little each year for 100 years."),
           ("a video of lava pouring down a volcano in one night", "fast", "It happened in one night."),
           ("an old photo of a big rock and a new photo of the same rock, only a bit smaller after 100 years", "slow", "It took 100 years to change a little."),
           ("a scientist's report that a rockslide closed a trail in a few seconds", "fast", "It took seconds.")]


def g_source():
    src, sp, why = R.choice(SOURCES)
    who = P.next()[0]
    if not once(src):
        return None
    return item("%s finds %s. Is this evidence of a fast change or a slow change?" % (who, src), sp, ["slow" if sp == "fast" else "fast", "no change at all", "a change made by people"], why)


def volcano(x, y, k=1.0, erupt=True):
    s = "<path d='M%g %g L%g %g L%g %g L%g %g Z' fill='#8a6d55' stroke='%s' stroke-width='2'/>" % (x - 60 * k, y + 40 * k, x - 14 * k, y - 30 * k, x + 14 * k, y - 30 * k, x + 60 * k, y + 40 * k, INK)
    if erupt:
        s += "<path d='M%g %g Q%g %g %g %g L%g %g Q%g %g %g %g Z' fill='#e2552d' stroke='%s' stroke-width='1.5'/>" % (
            x - 14 * k, y - 30 * k, x - 20 * k, y - 60 * k, x - 6 * k, y - 66 * k, x + 6 * k, y - 66 * k, x + 20 * k, y - 60 * k, x + 14 * k, y - 30 * k, INK)
        s += "<path d='M%g %g L%g %g L%g %g Z' fill='#e2552d'/>" % (x - 10 * k, y - 30 * k, x + 10 * k, y - 30 * k, x + 22 * k, y + 10 * k)
    return s


def canyon(x, y, k=1.0):
    s = "<path d='M%g %g L%g %g L%g %g L%g %g L%g %g L%g %g Z' fill='#d9925a' stroke='%s' stroke-width='2'/>" % (
        x - 70 * k, y - 30 * k, x - 18 * k, y - 30 * k, x - 8 * k, y + 30 * k, x + 8 * k, y + 30 * k, x + 18 * k, y - 30 * k, x + 70 * k, y - 30 * k, INK)
    s += "<path d='M%g %g L%g %g L%g %g L%g %g Z' fill='#d9925a' stroke='%s' stroke-width='2'/>" % (x - 70 * k, y - 30 * k, x - 70 * k, y + 40 * k, x + 70 * k, y + 40 * k, x + 70 * k, y - 30 * k, INK)
    s += "<path d='M%g %g L%g %g L%g %g L%g %g Z' fill='#e6f3fc' stroke='%s' stroke-width='2'/>" % (x - 18 * k, y - 30 * k, x - 8 * k, y + 30 * k, x + 8 * k, y + 30 * k, x + 18 * k, y - 30 * k, INK)
    s += "<rect x='%g' y='%g' width='%g' height='%g' fill='#5aa6d6'/>" % (x - 8 * k, y + 24 * k, 16 * k, 6 * k)
    for i in range(3):
        s += "<line x1='%g' y1='%g' x2='%g' y2='%g' stroke='#b06f3e' stroke-width='1.5'/>" % (x - 66 * k, y - 10 * k + i * 16 * k, x - 16 * k + i * 3 * k, y - 10 * k + i * 16 * k)
        s += "<line x1='%g' y1='%g' x2='%g' y2='%g' stroke='#b06f3e' stroke-width='1.5'/>" % (x + 16 * k - i * 3 * k, y - 10 * k + i * 16 * k, x + 66 * k, y - 10 * k + i * 16 * k)
    return s


PICS = {"volcano": (lambda x, y: volcano(x, y), "a volcano erupting", "fast", "hours or days"),
        "canyon": (lambda x, y: canyon(x, y), "a canyon with a river at the bottom", "slow", "millions of years"),
        "mountain": (lambda x, y: K.icon("mountain", x, y, 1.1), "a mountain", "slow", "millions of years"),
        "storm": (lambda x, y: K.icon("storm", x, y, 1.1), "a big storm that causes a flood", "fast", "hours or days")}


def pic_svg(kind):
    f, lab, _, _ = PICS[kind]
    return svg_wrap(200, 150, f(100, 82), lab)


def g_pic():
    kind = R.choice(sorted(PICS))
    _, lab, sp, t = PICS[kind]
    who = P.next()[0]
    k = R.choice(["speed", "time"])
    if not once((kind, k)):
        return None
    q = {"volcano": "This volcano erupts.", "canyon": "A river carved this canyon.", "mountain": "Wind and rain wear down this mountain.", "storm": "This storm floods a town."}[kind]
    if k == "speed":
        return item(fig(pic_svg(kind)) + "%s looks at this picture. %s Is it a fast change or a slow change?" % (who, q), sp, ["slow" if sp == "fast" else "fast", "It never changes.", "Only people can change it."],
                    "It takes %s." % t)
    bad = R.sample(SLOW_T if sp == "fast" else FAST_T, 2) + ["exactly one week"]
    return item(fig(pic_svg(kind)) + "%s looks at this picture. %s How long does it take?" % (who, q), t, bad, "It is a %s change." % sp)


def rock_svg(sizes, years):
    s = ""
    for i, (r, y) in enumerate(zip(sizes, years)):
        x = 70 + i * 130
        s += K.icon("rock", x, 70, r)
        s += text(x, 130, y, 14)
        if i:
            s += arrow(x - 85, 70, x - 45, 70, "#d9822b", 2.5, 8)
    return svg_wrap(130 * len(sizes), 145, s, "a rock getting smaller over " + ", ".join(years))


def g_rock():
    who = P.next()[0]
    gap = R.choice([50, 100, 200, 500, 1000])
    if not once(("r", gap)):
        return None
    pic = rock_svg([1.2, 1.05, 0.9], ["now", "%d years" % gap, "%d years" % (2 * gap)])
    if gap <= 100:
        return item(fig(pic) + "%s's book shows a rock wearing away. How many years until it looks like the last picture?" % who, "%d years" % (2 * gap), ["%d years" % gap, "%d years" % (3 * gap), "1 day"],
                    "%d + %d = %d years. Weathering is slow." % (gap, gap, 2 * gap))
    return item(fig(pic) + "%s's book shows a rock wearing away over %d years. What does this show?" % (who, 2 * gap), "Rocks wear away slowly.", ["Rocks wear away in one day.", "Rocks never change.", "Rocks get bigger."],
                "A little change over many years is a slow change.")


B1 = bank([
    ("Which change is fast?", "an earthquake", ["a canyon forming", "a mountain wearing down", "a glacier moving"], "Earthquakes last seconds or minutes."),
    ("Which change is slow?", "a river carving a canyon", ["a volcano erupting", "a landslide", "a flood"], "Canyons take millions of years."),
    ("What does 'weathering' mean?", "rock slowly breaking into smaller pieces", ["rain falling", "a hot day", "a rock growing"], "Wind, water and ice break rock."),
    ("What does 'erosion' mean?", "wind or water carrying rock and soil away", ["rock getting bigger", "plants growing", "snow falling"], "Bits are moved to new places."),
    ("Can a slow change still change the land a lot?", "Yes, over a very long time.", ["No, slow changes do nothing.", "Only if it is cold.", "Only in one day."], "Slow does not mean small."),
    ("How long can a big canyon take to form?", "millions of years", ["one day", "one week", "one hour"], "Rivers cut rock very slowly."),
    ("What can a volcano do in a few hours?", "cover land with lava", ["carve a canyon", "wear down a mountain", "make a glacier"], "Eruptions are fast."),
    ("Where can you find out about Earth changes?", "books, videos, photos and maps", ["only by guessing", "only in dreams", "nowhere"], "Use more than one source."),
])
B5 = bank([
    ("Ava's photo from 1950 and her photo from today show the same cliff, almost the same. What kind of change is the cliff having?", "slow", ["fast", "none ever", "a volcano"], "Very little change in many years."),
    ("Leo says the Grand Canyon formed in one big flood. Is he right?", "No. A river carved it over millions of years.", ["Yes.", "Yes, in one week.", "No, people dug it."], "Canyons form slowly."),
    ("Mia reads that a landslide covered a road in 2 minutes. Which word fits?", "fast", ["slow", "never", "weathering"], "2 minutes is fast."),
    ("A glacier moves 1 foot each day. How far does it move in 7 days?", "7 feet", ["1 foot", "14 feet", "70 feet"], "7 × 1 = 7. Still slow!"),
    ("Kai wants evidence that a beach is wearing away. Which source helps most?", "photos of the beach taken every year for 20 years", ["a picture of one shell", "a drawing of a fish", "a weather report for today"], "Photos over time show slow change."),
])


def body():
    pic = svg_wrap(420, 150, volcano(100, 82) + canyon(320, 82) + text(100, 146, "fast", 15) + text(320, 146, "slow", 15), "a volcano erupting (fast) and a canyon (slow)")
    ex = [("A volcano erupts. Fast or slow?", ["It takes hours or days."], "fast"),
          ("A river carves a canyon. Fast or slow?", ["It takes millions of years."], "slow")]
    mist = ["Thinking big changes, like canyons, happen fast.",
            "Thinking rocks never change.",
            "Thinking slow changes do not do much."]
    return kid_lesson(pic, "Ask: how long does the change take?",
                      ["Fast: volcano, earthquake, landslide, flood.", "Slow: canyon, weathering, glacier.", "Use books, photos and videos as evidence."], ex, mist)


def main():
    sets = U.sets([
        ("Fast or slow?", B1 + [(g_speed, 9), (g_pic, 3)]),
        ("How long does it take?", [(g_speed, 10), (g_pic, 2), (g_rock, 4), (g_which, 4)]),
        ("Comparing changes", [(g_which, 12), (g_speed, 8)]),
        ("Using evidence", [(g_source, 10), (g_which, 7), (g_rock, 1), (g_pic, 2)]),
        ("Earth detectives", B5 + [(g_which, 9), (g_pic, 1)]),
    ])
    make("grade-2", "fast-and-slow-earth-changes", 8, "2-ESS1-1",
         "Use information from several sources to provide evidence that Earth events can occur quickly or slowly.",
         "Fast and Slow Earth Changes",
         "Grade 2 Fast and Slow Earth Changes Worksheets: Volcanoes, Canyons and Erosion",
         "Fast and Slow Changes",
         "Free grade 2 science worksheets on fast and slow Earth changes (NGSS 2-ESS1-1): volcanoes, earthquakes, canyons and weathering, with evidence from books, photos and videos. 100 questions with answers.",
         "Some changes are fast. Some are slow.",
         "Volcanoes are fast. Canyons take millions of years.",
         body(),
         [("What are fast Earth changes?", "Volcanoes, earthquakes, landslides and floods change the land in seconds, hours or days."),
          ("What are slow Earth changes?", "Rivers carving canyons, rocks wearing into sand and glaciers moving take hundreds to millions of years."),
          ("How do we know?", "Books, videos, photos taken years apart and maps give us evidence.")],
         sets)


if __name__ == "__main__":
    main()
