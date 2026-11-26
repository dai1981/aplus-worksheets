# -*- coding: utf-8 -*-
"""
US Grade 4 Science: Earth's Features and Maps (4-ESS2-2)
  python tools/gen_us_science_g4_earths_features_and_maps.py
Maps help locate Earth's features: mountains, volcanoes, earthquakes, ocean trenches and ridges.
These features happen in patterns: many volcanoes and earthquakes lie in bands along the edges of
continents and oceans (the Ring of Fire around the Pacific), mountain chains lie along coasts or inside
continents, and long ridges run down the middle of oceans.
Map skills: map key (legend), symbols, elevation colors, compass directions.
Wrong answers come from real mistakes: "volcanoes are spread evenly everywhere", "the ocean floor is
flat", "the deepest places are in the middle of continents".
"""
from sci_common import Unit, item, bank, lesson, make, fig, figure, svg_wrap, rect, line, circle, text, People, INK, BLUE, RED

U = Unit(40114)
R = U.R
P = People(R)
SEA = "#cfe5f5"
LAND = "#e9dcb5"
DIR = {"west": "along the west coast", "east": "along the east coast", "north": "along the north coast", "south": "along the south coast"}


def tri(x, y, col="#7a5a3a", s=9):
    return "<path d='M%.1f %.1f L%.1f %.1f L%.1f %.1f Z' fill='%s' stroke='%s' stroke-width='1'/>" % (x - s, y + s * 0.8, x, y - s * 0.9, x + s, y + s * 0.8, col, INK)


def compass(x, y):
    return (line(x, y - 14, x, y + 14, INK, 1.5) + line(x - 14, y, x + 14, y, INK, 1.5)
            + text(x, y - 18, "N", 11) + text(x, y + 26, "S", 11) + text(x - 21, y + 4, "W", 11) + text(x + 21, y + 4, "E", 11))


def island_map(side, feature, label):
    """A made-up continent with a band of `feature` symbols along one coast."""
    W, H = 360, 260
    x0, y0, x1, y1 = 60, 60, 280, 235
    H = 255
    s = [rect(0, 0, W, H, SEA, INK, 1.5), rect(x0, y0, x1 - x0, y1 - y0, LAND, INK, 1.5, 18), compass(325, 36)]
    pts = []
    if side in ("west", "east"):
        x = x0 + 16 if side == "west" else x1 - 16
        pts = [(x + R.randint(-5, 5), y) for y in range(y0 + 18, y1 - 10, 22)]
    else:
        y = y0 + 18 if side == "north" else y1 - 18
        pts = [(x, y + R.randint(-4, 4)) for x in range(x0 + 22, x1 - 10, 24)]
    pts += [(R.randint(x0 + 70, x1 - 70), R.randint(y0 + 60, y1 - 60))]
    for (x, y) in pts:
        if feature == "volcano":
            s.append(tri(x, y, RED, 8))
        elif feature == "mountain":
            s.append(tri(x, y))
        else:
            s.append(circle(x, y, 5, "#f0a030", INK, 1))
    # a few scattered others
    s.append(rect(8, 8, 120, 34, "#fff", INK, 1))
    sym = {"volcano": tri(22, 25, RED, 7), "mountain": tri(22, 25), "earthquake": circle(22, 25, 5, "#f0a030", INK, 1)}[feature]
    s.append(sym + text(36, 29, {"volcano": "volcano", "mountain": "mountain", "earthquake": "earthquake"}[feature], 12, "start", weight=400))
    return svg_wrap(W, H, "".join(s), label).replace("<svg ", "<svg data-pf='lg' ", 1)


def g_band():
    side = R.choice(sorted(DIR))
    f = R.choice(["volcano", "mountain", "earthquake"])
    pl = {"volcano": "volcanoes", "mountain": "mountains", "earthquake": "earthquakes"}[f]
    land = R.choice(["Island X", "Kana Island", "Tull Island", "Mora Island", "Zev Island"])
    return item(fig(island_map(side, f, "a map of %s showing %s" % (land, pl))) + "This map of %s shows where %s are. What pattern do you see?" % (land, pl),
                "Most of them are in a line %s." % DIR[side], ["Most of them are in a line %s." % DIR[x] for x in R.sample([d for d in DIR if d != side], 2)]
                + ["They are spread evenly over the whole island."], "The symbols form a band %s. Features like these often form in long chains." % DIR[side])


ELEV = [("0–100 m", "#b9dfa0"), ("100–500 m", "#f1e6a2"), ("500–1,000 m", "#e0b071"), ("over 1,000 m", "#b07a4a")]


def elev_map():
    """4x5 grid of elevation colors; a ridge of high land runs along one column or row."""
    rows, cols = 4, 5
    kind = R.choice(["col", "row"])
    k = R.randrange(cols if kind == "col" else rows)
    grid = []
    for r in range(rows):
        line_ = []
        for c in range(cols):
            d = abs(c - k) if kind == "col" else abs(r - k)
            line_.append(max(0, 3 - d))
        grid.append(line_)
    cw, ch = 50, 40
    s = []
    for r in range(rows):
        for c in range(cols):
            s.append(rect(10 + c * cw, 10 + r * ch, cw, ch, ELEV[grid[r][c]][1], "#888", 0.5))
    for c in range(cols):
        s.append(text(10 + c * cw + cw / 2, 10 + rows * ch + 16, "ABCDE"[c], 12))
    for r in range(rows):
        s.append(text(2 + cols * cw + 18, 10 + r * ch + ch / 2 + 4, str(r + 1), 12))
    kx = 10 + cols * cw + 34
    for i, (lab, col) in enumerate(reversed(ELEV)):
        s.append(rect(kx, 12 + i * 22, 16, 14, col, "#888", 0.5) + text(kx + 22, 24 + i * 22, lab, 11, "start", weight=400))
    W = kx + 110
    return svg_wrap(W, 10 + rows * ch + 26, "".join(s), "an elevation map with a key"), kind, k, grid


def g_elev():
    svg, kind, k, grid = elev_map()
    place = R.choice(["Pine Valley", "Red Rock County", "the Blue Hills", "Cedar Island", "Fox Plains", "Eagle Park", "Stone Lake", "Mesa Land"])
    q = R.choice(["where", "low"])
    if q == "where":
        a = "in column %s" % "ABCDE"[k] if kind == "col" else "in row %d" % (k + 1)
        if kind == "col":
            w = ["in column %s" % x for x in R.sample([x for x in "ABCDE" if x != "ABCDE"[k]], 2)]
        else:
            w = ["in row %d" % x for x in R.sample([x for x in range(1, 5) if x != k + 1], 2)]
        return item(fig(svg) + "This elevation map shows %s. Use the map key. Where is the highest land?" % place, a, w + ["all over the map equally"],
                    "The darkest brown (over 1,000 m) forms a line %s. This is a mountain range." % a)
    lows = [(r, c) for r in range(4) for c in range(5) if grid[r][c] == 0]
    highs = [(r, c) for r in range(4) for c in range(5) if grid[r][c] == 3]
    mids = [(r, c) for r in range(4) for c in range(5) if grid[r][c] in (1, 2)]
    if not lows or len(mids) < 2:
        return None
    r, c = R.choice(lows)
    a = "%s%d" % ("ABCDE"[c], r + 1)
    w = ["%s%d" % ("ABCDE"[cc], rr + 1) for rr, cc in [R.choice(highs)] + R.sample(mids, 2)]
    return item(fig(svg) + "This elevation map shows %s. Use the map key. Which square has the lowest land (0–100 m)?" % place, a, w,
                "Square %s is light green, which the key shows is 0–100 m." % a)


FACTS = [("Where are most of the world's active volcanoes?", "in a ring around the edges of the Pacific Ocean", ["spread evenly across every continent", "only in the middle of Africa", "only near the North Pole"],
          "This band of volcanoes and earthquakes is called the Ring of Fire."),
         ("What is the Ring of Fire?", "a band of many volcanoes and earthquakes around the Pacific Ocean", ["a ring of forest fires in Canada", "a circle of deserts", "the path of the sun"],
          "It follows the edges of the Pacific Ocean."),
         ("Where are the Andes Mountains?", "along the west coast of South America", ["in the middle of the Pacific Ocean", "along the east coast of Africa", "in Antarctica only"],
          "The Andes run in a long chain along the western edge of South America."),
         ("Where are the Rocky Mountains?", "in the western part of North America", ["along the east coast of the United States", "in Australia", "in the middle of the Atlantic Ocean"],
          "The Rockies run north to south in the west."),
         ("What is a mid-ocean ridge?", "a long chain of underwater mountains", ["a deep hole in a continent", "a sandy beach", "a river delta"],
          "The Mid-Atlantic Ridge runs down the middle of the Atlantic Ocean."),
         ("Where is the deepest place in the ocean?", "the Mariana Trench in the Pacific Ocean", ["the middle of the Atlantic Ridge", "a lake in Africa", "the top of Mount Everest"],
          "Trenches are very deep valleys in the ocean floor."),
         ("Is the ocean floor flat?", "No. It has mountains, ridges, trenches and plains.", ["Yes, it is completely flat.", "Yes, but only in the Pacific.", "It is covered only by ice."],
          "Maps of the ocean floor show many features."),
         ("Earthquakes and volcanoes are often found", "in the same places, in long bands", ["far from each other", "only in deserts", "only where there are no mountains"],
          "Maps show they form similar patterns."),
         ("What do the brown and dark colors on a relief map usually show?", "high land, like mountains", ["deep oceans", "cities", "rivers"], "Map keys show what each color means."),
         ("What is a map key (legend)?", "a box that explains the symbols and colors on a map", ["the title of a map", "a compass", "a scale bar only"], "Always read the key first."),
         ("Which tool shows directions on a map?", "a compass rose", ["a map key", "a scale bar", "the title"], "It shows north, south, east and west."),
         ("What is a trench?", "a long, very deep valley in the ocean floor", ["a tall mountain on land", "a flat plain", "a lake"], "Trenches are the deepest parts of the ocean."),
         ("Where are the Himalayas, the tallest mountains on Earth?", "in Asia", ["in South America", "in the Atlantic Ocean", "in Australia"], "Mount Everest is in the Himalayas."),
         ("Why do scientists make maps of earthquakes?", "to find patterns that show where earthquakes are likely", ["to make earthquakes stop", "to decorate classrooms", "to measure rain"],
          "Patterns help people prepare."),
         ("Many volcanoes on a map lie in a line along a coast. What does this pattern help scientists predict?", "where new volcanoes or eruptions are more likely", ["the weather tomorrow", "where rivers start", "which animals live there"],
          "Patterns on maps help us make predictions.")]
B1 = __import__("sci_common").bank(FACTS)
B5 = __import__("sci_common").bank([
    ("Ava looks at a world map of earthquakes. Most dots are around the Pacific Ocean. What should she conclude?", "Earthquakes happen more often in some places than others.", ["Earthquakes happen equally everywhere.", "Earthquakes only happen in oceans.", "The map is wrong."],
     "The dots form a pattern."),
    ("Leo compares a volcano map and an earthquake map. What does he notice?", "Many volcanoes and earthquakes are in the same areas.", ["They are never in the same areas.", "Volcanoes are only in deserts.", "Earthquakes are only at the poles."],
     "Both follow the edges of the Pacific and other bands."),
    ("A map shows mountains along the west coast of a continent and flat plains in the middle. Where would you expect more earthquakes?", "near the mountains on the west coast", ["in the flat plains", "far out in the ocean only", "nowhere"],
     "Mountain chains along coasts often have earthquakes and volcanoes."),
    ("Mia wants to find the deepest part of an ocean. What kind of map should she use?", "a map of the ocean floor that shows depth", ["a road map", "a weather map", "a map of state capitals"],
     "Depth maps show trenches and ridges."),
    ("Why might a town near a volcano chain need an emergency plan?", "Maps show eruptions and earthquakes are more likely there.", ["Volcanoes never erupt.", "Maps show it will snow.", "The town is far from all hazards."],
     "Map patterns help communities prepare."),
])


def body():
    think = ("<p><b>Maps</b> show where Earth's features are. Read the <b>map key</b> to learn what each symbol and color means, and use the <b>compass rose</b> for directions.</p>"
             "<p>Earth's features are not spread out evenly. They form <b>patterns</b>:</p>"
             "<ul><li>Many <b>volcanoes</b> and <b>earthquakes</b> are in long bands, like the <b>Ring of Fire</b> around the Pacific Ocean.</li>"
             "<li><b>Mountain chains</b> often run along the edges of continents, like the Andes and the Rockies.</li>"
             "<li>The ocean floor has <b>ridges</b> (underwater mountain chains) and <b>trenches</b> (very deep valleys).</li></ul>"
             + figure(island_map("west", "volcano", "a map with volcanoes along the west coast"), "On this map, the volcanoes form a line along the west coast."))
    ex = [("A map shows earthquake dots in a band around the Pacific Ocean. What is the pattern?", ["The dots are not everywhere.", "They follow the edge of the Pacific."], "Most earthquakes are around the edges of the Pacific."),
          ("On an elevation map, dark brown means over 1,000 m. A line of dark brown runs north to south. What is it?", ["Dark brown = high land."], "a mountain range")]
    mist = ["Thinking volcanoes and earthquakes are spread evenly over Earth.",
            "Thinking the ocean floor is flat.",
            "Forgetting to read the map key before answering."]
    return lesson(think, ex, mist)


def main():
    sets = U.sets([
        ("Earth's features", B1 + [(g_band, 5)]),
        ("Patterns on maps", [(g_band, 12), (g_elev, 8)]),
        ("Reading elevation maps", [(g_elev, 14), (g_band, 6)]),
        ("Volcanoes, earthquakes and mountains", [(g_band, 10), (g_elev, 10)]),
        ("Using maps to predict", B5 + [g_band, g_elev]),
    ])
    make("grade-4", "earths-features-and-maps", 14, "4-ESS2-2",
         "Analyze and interpret data from maps to describe patterns of Earth's features.",
         "Earth's Features and Maps",
         "Grade 4 Earth's Features Worksheets: Mountains, Volcanoes, Earthquakes and Map Patterns",
         "Earth's Features and Maps",
         "Free Grade 4 science worksheets on Earth's features and maps (NGSS 4-ESS2-2): map keys and elevation maps, patterns of mountains, volcanoes and earthquakes, the Ring of Fire, ocean ridges and trenches. 100 practice questions with answers.",
         "Earth's features form patterns on maps.",
         "Many volcanoes and earthquakes lie in long bands, like the Ring of Fire around the Pacific. Mountains often form chains.",
         body(),
         [("What patterns do maps show about volcanoes and earthquakes?", "They are mostly found in long bands, such as the Ring of Fire around the Pacific Ocean, not spread evenly over Earth."),
          ("What features are on the ocean floor?", "Mid-ocean ridges (long underwater mountain chains), deep trenches, and wide flat plains."),
          ("How do you read an elevation map?", "Use the map key. Each color stands for a range of heights, so you can find mountains and low land.")],
         sets)


if __name__ == "__main__":
    main()
