# -*- coding: utf-8 -*-
"""
UK Year 1 science: The Four Seasons (Seasonal changes)
  python tools/gen_uk_science_y1_four_seasons.py
Observe changes across the four seasons: the order of the seasons, which months are in each season in the UK, signs of
each season in nature (blossom, lambs, falling leaves, frost), what to wear, and a table of trees through the year.
Wrong answers come from real mistakes: "spring comes after summer", "December is in autumn", "leaves fall in spring",
"it is always cold in winter and hot in summer everywhere in the world".
"""
from uk_sci import Unit, item, bank, kid_lesson, make_uk, table, People, once
import sci_kids as K

U = Unit(61111)
R = U.R
P = People(R)

SEAS = ["spring", "summer", "autumn", "winter"]


def g_order():
    i = R.randrange(4)
    k = R.random() < 0.5
    if not once(("or", i, k)):
        return None
    if k:
        a = SEAS[(i + 1) % 4]
        return item("Which season comes after %s?" % SEAS[i], a, [x for x in SEAS if x != a], "Spring, summer, autumn, winter, then spring again.")
    a = SEAS[(i - 1) % 4]
    return item("Which season comes before %s?" % SEAS[i], a, [x for x in SEAS if x != a], "Spring, summer, autumn, winter, then spring again.")


MONTH = [("January", "winter"), ("February", "winter"), ("March", "spring"), ("April", "spring"), ("May", "spring"), ("June", "summer"), ("July", "summer"),
         ("August", "summer"), ("September", "autumn"), ("October", "autumn"), ("November", "autumn"), ("December", "winter")]


def g_month():
    m, s = R.choice(MONTH)
    if not once(("mo", m)):
        return None
    return item("In the UK, which season is %s in?" % m, s, [x for x in SEAS if x != s], "Spring: March–May. Summer: June–August. Autumn: September–November. Winter: December–February.")


SIGN = [("Blossom appears on the trees and lambs are born.", "spring"), ("Daffodils and bluebells flower.", "spring"), ("Birds build nests and frogspawn appears in ponds.", "spring"),
        ("The days are long and hot, and people go to the beach.", "summer"), ("Strawberries are ripe and ready to pick.", "summer"),
        ("Leaves turn red, orange and brown and fall off the trees.", "autumn"), ("Conkers and acorns fall to the ground.", "autumn"), ("Squirrels bury nuts for later.", "autumn"),
        ("There is frost on the grass in the morning.", "winter"), ("It might snow, and ponds can freeze.", "winter"), ("Hedgehogs are hibernating.", "winter"),
        ("The days are shortest and it gets dark before tea time.", "winter")]


def g_sign():
    s, a = R.choice(SIGN)
    if not once(("si", s)):
        return None
    return item("%s Which season is it?" % s, a, [x for x in SEAS if x != a], "Each season brings changes in plants, animals and the weather.")


WEAR = [("a thick coat, a woolly hat and gloves", "winter"), ("shorts, a sun hat and sun cream", "summer"), ("a light jacket and wellies for April showers", "spring"),
        ("a warm jumper and a raincoat for windy, wet days", "autumn")]


def g_wear():
    w, a = R.choice(WEAR)
    k = R.random() < 0.5
    if not once(("we", w, k)):
        return None
    if k:
        return item("In which season would you most likely wear %s?" % w, a, [x for x in SEAS if x != a], "We dress for the weather.")
    return item("What would be best to wear on a cold, snowy day in %s?" % a if a == "winter" else "What would be best to wear on a hot, sunny day in %s?" % a if a == "summer" else
                "What would be best to wear in %s?" % a, w, [x[0] for x in WEAR if x[0] != w], "We dress for the weather.")


TREE = [("spring", "small new leaves and blossom"), ("summer", "lots of big green leaves"), ("autumn", "red, orange and brown leaves falling off"), ("winter", "bare branches with no leaves")]


def g_tree():
    who = P.next()[0]
    rows = TREE[:]
    k = R.choice(SEAS + ["bare", "colour"])
    if not once(("tr", k, who)) or not once(("tk", k), 3):
        return None
    tab = table(["Season", "What the oak tree looked like"], [[s, d] for s, d in rows])
    intro = tab + "%s looked at the same oak tree in every season. " % who
    if k in SEAS:
        a = dict(TREE)[k]
        return item(intro + "What did the oak tree look like in %s?" % k, a, [d for s, d in TREE if s != k], "Read the table.")
    if k == "bare":
        return item(intro + "In which season did the tree have no leaves?", "winter", ["spring", "summer", "autumn"], "Oak trees are deciduous.")
    return item(intro + "In which season did the leaves change colour?", "autumn", ["spring", "summer", "winter"], "Leaves change colour and fall in autumn.")


TEMPS = {"January": 5, "April": 11, "July": 20, "October": 13}


def g_temp():
    who = P.next()[0]
    ms = ["January", "April", "July", "October"]
    v = [TEMPS[m] + R.choice([-2, -1, 0, 1, 2]) for m in ms]
    if len(set(v)) < 4:
        return None
    k = R.choice(["warm", "cold", "read", "season", "diff"])
    ri = R.randrange(4)
    if not once(("te", tuple(v), k, ri if k in ("read", "season") else 0)):
        return None
    tab = table(["Month", "Temperature at midday (°C)"], [[m, str(x)] for m, x in zip(ms, v)])
    intro = tab + "%s's class measured the temperature at midday in four months. " % who
    if k == "warm":
        a = ms[v.index(max(v))]
        return item(intro + "Which month was the warmest?", a, [x for x in ms if x != a], "The biggest number of degrees.")
    if k == "cold":
        a = ms[v.index(min(v))]
        return item(intro + "Which month was the coldest?", a, [x for x in ms if x != a], "The smallest number of degrees.")
    if k == "read":
        g = "%d °C" % v[ri]
        return item(intro + "What was the temperature in %s?" % ms[ri], g, ["%d °C" % x for x in v if x != v[ri]][:3], "Read the row.")
    if k == "season":
        a = dict(MONTH)[ms[ri]]
        return item(intro + "Which season is %s in?" % ms[ri], a, [x for x in SEAS if x != a], "Use the months of each season.")
    d = max(v) - min(v)
    g = "%d °C" % d
    return item(intro + "How much warmer was the warmest month than the coldest month?", g, [x for x in dict.fromkeys(["%d °C" % max(v), "%d °C" % min(v), "%d °C" % (d + 2), "%d °C" % (max(v) + min(v))]) if x != g][:3],
                "%d − %d = %d." % (max(v), min(v), d))


B1 = bank([
    ("How many seasons are there in a year?", "four", ["two", "six", "twelve"], "Spring, summer, autumn, winter."),
    ("Which season is usually the warmest in the UK?", "summer", ["winter", "autumn", "spring"], "Long, sunny days."),
    ("Which season is usually the coldest in the UK?", "winter", ["summer", "spring", "autumn"], "Frost and maybe snow."),
    ("In which season do many trees lose their leaves?", "autumn", ["spring", "summer", "winter"], "Leaves fall in autumn."),
    ("In which season do many baby animals like lambs appear?", "spring", ["autumn", "winter", "summer"], "New life."),
    ("Which season comes after winter?", "spring", ["autumn", "summer", "winter again"], "Then summer."),
    ("Which season has Christmas in the UK?", "winter", ["summer", "spring", "autumn"], "December."),
    ("Which season has the longest days?", "summer", ["winter", "autumn", "spring"], "It stays light late."),
])
B5 = bank([
    ("Why do some animals hibernate in winter?", "There is little food, so they sleep through the cold months.", ["They are on holiday.", "They are too hot.", "They hate snow."], "Hedgehogs hibernate."),
    ("Why do some birds fly away in autumn?", "They fly to warmer places where there is more food.", ["They are lost.", "They want to see snow.", "They are too warm."], "Migration."),
    ("How could you record how a tree changes through the year?", "Take a photo or draw it in every season.", ["Look at it once.", "Cut it down.", "Guess."], "Observe over time."),
    ("Is it summer everywhere in the world in July?", "No. In Australia, July is winter.", ["Yes, everywhere.", "Only in the UK.", "Yes, it is always summer."], "Seasons differ round the world."),
    ("Why do farmers plant many seeds in spring?", "It is getting warmer and lighter, so seeds can grow.", ["It is coldest then.", "There is snow to water them.", "Seeds only grow in the dark."], "Warmth and light."),
])


def body():
    pic = K.row(["sprout", "sun", "leaf", "snow"], words=["spring", "summer", "autumn", "winter"], size=80, label="spring, summer, autumn and winter")
    ex = [("Which season comes after summer?", ["Leaves fall next"], "autumn"),
          ("Frost on the grass. Which season?", ["Coldest season"], "winter")]
    mist = ["Thinking spring comes after summer.", "Thinking December is in autumn.", "Thinking leaves fall in spring."]
    return kid_lesson(pic, "There are four seasons in a year.",
                      ["Spring, summer, autumn, winter.", "Each season has different weather.", "Plants and animals change with the seasons."], ex, mist)


def main():
    sets = U.sets([
        ("The four seasons", B1 + [(g_order, 8), (g_wear, 4)]),
        ("Months and seasons", [(g_month, 12), (g_sign, 8)]),
        ("Signs of the seasons", [(g_sign, 4), (g_wear, 4), (g_tree, 10), (g_temp, 2)]),
        ("Temperature through the year", [(g_temp, 20)]),
        ("Thinking about seasons", B5 + [(g_tree, 4), (g_temp, 11)]),
    ])
    make_uk(1, "four-seasons", 11, "Seasonal changes",
            "Observe changes across the four seasons. Observe and describe weather associated with the seasons and how day length varies.",
            "The Four Seasons",
            "Year 1 Science: The Four Seasons Worksheets (Spring, Summer, Autumn, Winter)",
            "The Four Seasons",
            "Free Year 1 science worksheets on the four seasons: the order of the seasons, months, signs of each season in nature, what to wear and temperature through the year. 100 questions with answers.",
            "There are four seasons.",
            "Spring, summer, autumn and winter, then spring again.",
            body(),
            [("What are the four seasons?", "Spring, summer, autumn and winter. They come in the same order every year."),
             ("Which months are in each season in the UK?", "Spring: March, April, May. Summer: June, July, August. Autumn: September, October, November. Winter: December, January, February."),
             ("How do plants and animals change with the seasons?", "In spring there is blossom and baby animals; in summer lots of green leaves; in autumn leaves fall and squirrels store nuts; in winter many trees are bare and some animals hibernate.")],
            sets)


if __name__ == "__main__":
    main()
