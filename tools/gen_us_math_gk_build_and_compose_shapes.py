# -*- coding: utf-8 -*-
"""
US Kindergarten Math: Build and Compose Shapes (K.G.B.5, K.G.B.6)
  python3 tools/gen_us_math_gk_build_and_compose_shapes.py
Build shapes with sticks and clay balls (sides and corners), find the small shapes inside a big shape,
count the parts, and put small shapes together to make a bigger shape.
"""
import math, random
from ws_common import table, write_unit, fig, svg_wrap, text
from k_pics import SHAPE_COL
from k_common import Kids, mcq, finish

UPDATED = "2026-11-16"
U = 44
H3 = math.sqrt(3)
COLS = ["red", "blue", "yellow", "green", "red", "blue"]

# whole: (whole name, part name, number of parts, polygons in units)
FIG = {
    "sq2tri": ("square", "triangle", 2, [[(0, 0), (2, 0), (2, 2)], [(0, 0), (0, 2), (2, 2)]]),
    "rect2sq": ("rectangle", "square", 2, [[(0, 0), (2, 0), (2, 2), (0, 2)], [(2, 0), (4, 0), (4, 2), (2, 2)]]),
    "rect2tri": ("rectangle", "triangle", 2, [[(0, 0), (4, 0), (4, 2)], [(0, 0), (0, 2), (4, 2)]]),
    "hex6tri": ("hexagon", "triangle", 6, [[(0, 0), (2 * math.cos(math.pi / 3 * k), 2 * math.sin(math.pi / 3 * k)),
                                             (2 * math.cos(math.pi / 3 * (k + 1)), 2 * math.sin(math.pi / 3 * (k + 1)))]
                                            for k in range(6)]),
    "tri4tri": ("triangle", "triangle", 4, [[(0, 2 * H3), (1, H3), (2, 2 * H3)], [(1, H3), (2, 0), (3, H3)],
                                             [(2, 2 * H3), (3, H3), (4, 2 * H3)], [(1, H3), (3, H3), (2, 2 * H3)]]),
    "sq4sq": ("square", "square", 4, [[(0, 0), (2, 0), (2, 2), (0, 2)], [(2, 0), (4, 0), (4, 2), (2, 2)],
                                       [(0, 2), (2, 2), (2, 4), (0, 4)], [(2, 2), (4, 2), (4, 4), (2, 4)]]),
    "rect3sq": ("rectangle", "square", 3, [[(0, 0), (2, 0), (2, 2), (0, 2)], [(2, 0), (4, 0), (4, 2), (2, 2)],
                                            [(4, 0), (6, 0), (6, 2), (4, 2)]]),
    "sq2rect": ("square", "rectangle", 2, [[(0, 0), (4, 0), (4, 2), (0, 2)], [(0, 2), (4, 2), (4, 4), (0, 4)]]),
    "tri2tri": ("triangle", "triangle", 2, [[(0, 2 * H3), (2, 0), (2, 2 * H3)], [(2, 0), (4, 2 * H3), (2, 2 * H3)]]),
    "rect4sq": ("rectangle", "square", 4, [[(2 * k, 0), (2 * k + 2, 0), (2 * k + 2, 2), (2 * k, 2)] for k in range(4)]),
    "sq4tri": ("square", "triangle", 4, [[(0, 0), (4, 0), (2, 2)], [(4, 0), (4, 4), (2, 2)], [(4, 4), (0, 4), (2, 2)],
                                          [(0, 4), (0, 0), (2, 2)]]),
}


def poly_svg(polys, label, gap=0.0, unit=U):
    """Draw polygons (in units). gap > 0 pulls the pieces apart from the middle."""
    xs = [x for p in polys for x, _ in p]
    ys = [y for p in polys for _, y in p]
    cx0, cy0 = (min(xs) + max(xs)) / 2, (min(ys) + max(ys)) / 2
    moved = []
    for p in polys:
        px = sum(x for x, _ in p) / len(p) - cx0
        py = sum(y for _, y in p) / len(p) - cy0
        moved.append([(x + gap * px, y + gap * py) for x, y in p])
    xs = [x for p in moved for x, _ in p]
    ys = [y for p in moved for _, y in p]
    m = 10
    W = (max(xs) - min(xs)) * unit + 2 * m
    H = (max(ys) - min(ys)) * unit + 2 * m
    s = []
    for i, p in enumerate(moved):
        f, st = SHAPE_COL[COLS[i % len(COLS)]]
        pts = " ".join("%.1f,%.1f" % ((x - min(xs)) * unit + m, (y - min(ys)) * unit + m) for x, y in p)
        s.append("<polygon points='%s' fill='%s' stroke='#2b2b2b' stroke-width='2' stroke-linejoin='round'/>" % (pts, f))
    return svg_wrap(int(W), int(H), "".join(s), label)


def whole_svg(key, gap=0.0):
    w, part, n, polys = FIG[key]
    return poly_svg(polys, "a %s made of %d %ss" % (w, n, part) if not gap else "%d %ss" % (n, part), gap)


STICK = {"triangle": [(0, 2), (1.2, 0), (2.4, 2)], "square": [(0, 0), (2, 0), (2, 2), (0, 2)],
         "rectangle": [(0, 0), (3.4, 0), (3.4, 1.7), (0, 1.7)],
         "hexagon": [(1 + math.cos(math.pi / 3 * k), 1 + math.sin(math.pi / 3 * k)) for k in range(6)]}
SIDES = {"triangle": 3, "square": 4, "rectangle": 4, "hexagon": 6}


def sticks_svg(kind):
    pts = STICK[kind]
    m, u = 18, 52
    xs, ys = [x for x, _ in pts], [y for _, y in pts]
    P = [((x - min(xs)) * u + m, (y - min(ys)) * u + m) for x, y in pts]
    s = []
    for i in range(len(P)):
        a, b = P[i], P[(i + 1) % len(P)]
        s.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='#a0522d' stroke-width='7' stroke-linecap='round'/>"
                 % (a[0], a[1], b[0], b[1]))
    for x, y in P:
        s.append("<circle cx='%.1f' cy='%.1f' r='9' fill='#e78fb3' stroke='#a8476f' stroke-width='1.6'/>" % (x, y))
    return svg_wrap(int((max(xs) - min(xs)) * u + 2 * m), int((max(ys) - min(ys)) * u + 2 * m), "".join(s),
                    "a shape made of sticks and clay balls")


def cap(s):
    return s[0].upper() + s[1:]


def parts(n, part):
    return "%d %s" % (n, part + ("s" if n != 1 else ""))


# ============================================================ set 1: sticks and clay
def set_sticks(rnd, K):
    its = []
    for k in ["triangle", "square", "rectangle", "hexagon", "triangle", "square", "hexagon", "rectangle"]:
        n = SIDES[k]
        if len([x for x in its if k in x["q"]]) == 0:
            q, ans, wr = "How many <b>sticks</b> make this %s?" % k, n, [n + 1, n - 1, n + 2, 2 * n]
            e = "Each side is 1 stick. A %s has %d sides, so it needs <b>%d</b> sticks." % (k, n, n)
        else:
            q, ans, wr = "How many <b>clay balls</b> hold this %s together?" % k, n, [n + 1, n - 1, 2 * n, n + 2]
            e = "A clay ball goes at each corner. A %s has %d corners, so it needs <b>%d</b> clay balls." % (k, n, n)
        its.append(mcq(fig(sticks_svg(k)) + q, ans, wr, e))
    for k in ["triangle", "square", "rectangle", "hexagon"]:
        q = fig(sticks_svg(k)) + "What shape did the sticks make?"
        others = [x for x in ["Triangle", "Square", "Rectangle", "Hexagon", "Circle"] if x != cap(k)]
        e = "It has %d sides and %d corners%s. It is a <b>%s</b>." % (
            SIDES[k], SIDES[k], " that are all the same length" if k == "square" else
            (", 2 long and 2 short sides" if k == "rectangle" else ""), k)
        its.append(mcq(q, cap(k), others, e))
    for n, ans, wr, e in [
        (3, "Triangle", ["Square", "Hexagon", "Circle"], "3 sticks make 3 sides. A shape with 3 sides is a <b>triangle</b>."),
        (6, "Hexagon", ["Triangle", "Square", "Rectangle"], "6 sticks make 6 sides. A shape with 6 sides is a <b>hexagon</b>."),
    ]:
        p = K.next()
        its.append(mcq(fig(sticks_svg(ans.lower())) + "%s uses %d sticks of the same length. What shape can %s make?" % (p["n"], n, p["he"]),
                       ans, wr, e))
    for q, ans, wr, e in [
        ("Can you make a circle with straight sticks?", "No, a circle has no straight sides",
         ["Yes, with 4 sticks", "Yes, with 3 sticks", "Yes, with 1 stick"],
         "A circle is round. <b>No, a circle has no straight sides</b>, so we use clay or a string."),
        ("How many sticks do you need to make 2 triangles that do not touch?", "6",
         ["3", "5", "4"], "Each triangle needs 3 sticks. 3 + 3 = <b>6</b>."),
        ("Which shape needs the most sticks?", "Hexagon", ["Triangle", "Square", "Rectangle"],
         "A triangle needs 3, a square and a rectangle need 4, and a <b>hexagon</b> needs 6."),
        ("Which shape needs the fewest sticks?", "Triangle", ["Square", "Rectangle", "Hexagon"],
         "A <b>triangle</b> needs only 3 sticks. The others need 4 or 6."),
        ("You have 4 sticks of the same length. What shape can you make?", "Square", ["Triangle", "Hexagon", "Circle"],
         "4 sides that are all the same length make a <b>square</b>."),
        ("You have 2 long sticks and 2 short sticks. What shape can you make?", "Rectangle", ["Square", "Triangle", "Hexagon"],
         "2 long and 2 short sides make a <b>rectangle</b>."),
    ]:
        pic = sticks_svg({"Square": "square", "Rectangle": "rectangle"}.get(ans, "triangle")) if ans in ("Square", "Rectangle") else ""
        its.append(mcq((fig(pic) if pic else "") + q, ans, wr, e))
    o = its
    order = [o[0], o[8], o[1], o[9], o[4], o[5], o[14], o[2], o[10], o[12],
             o[18], o[19], o[6], o[3], o[11], o[13], o[7], o[16], o[17], o[15]]
    assert len({id(x) for x in order}) == 20
    return {"title": "Build with sticks and clay", "items": order}


# ============================================================ set 2: name the parts
def set_parts(rnd, K):
    its = []
    for key in ["sq2tri", "rect2sq", "rect2tri", "hex6tri", "tri2tri", "sq4sq", "rect3sq", "sq2rect", "tri4tri",
                "sq4tri", "rect4sq"]:
        w, part, n, _ = FIG[key]
        ans = parts(n, part)
        wr = [parts(n, p) for p in ["triangle", "square", "rectangle", "circle"] if p != part][:2] + \
            [parts(n + 1, part), parts(n - 1, part) if n > 2 else parts(n + 2, part)]
        q = fig(whole_svg(key)) + "This %s is made of smaller shapes. What are they?" % w
        e = "Look at the lines inside. Each piece is a %s. There are %d. The answer is <b>%s</b>." % (part, n, ans)
        its.append(mcq(q, ans, wr, e))
    for key in ["sq2tri", "rect2sq", "hex6tri", "tri2tri", "rect2tri", "sq2rect", "sq4sq", "rect3sq", "tri4tri"]:
        w, part, n, _ = FIG[key]
        q = fig(whole_svg(key)) + "What shape is each small piece?"
        others = [cap(x) for x in ["triangle", "square", "rectangle", "circle", "hexagon"] if x != part]
        e = "Count the sides of one piece. It is a <b>%s</b>." % part
        its.append(mcq(q, cap(part), others, e))
    o = its
    order = [o[0], o[11], o[1], o[12], o[2], o[15], o[4], o[14], o[3], o[13],
             o[7], o[16], o[6], o[18], o[5], o[17], o[8], o[19], o[9], o[10]]
    assert len({id(x) for x in order}) == 20
    return {"title": "Shapes inside shapes", "items": order}


# ============================================================ set 3: how many parts?
def set_count(rnd, K):
    its = []
    for key in ["sq2tri", "rect2sq", "rect3sq", "sq4sq", "hex6tri", "tri4tri", "rect4sq", "sq4tri", "tri2tri", "sq2rect"]:
        w, part, n, _ = FIG[key]
        q = fig(whole_svg(key)) + "How many <b>%ss</b> make this %s?" % (part, w)
        e = "Touch each %s and count: %s. <b>%d</b> %ss make the %s." % (
            part, ", ".join(str(k) for k in range(1, n + 1)), n, part, w)
        its.append(mcq(q, n, [n + 1, n - 1, n + 2, 2 * n], e))
    for key in ["sq2tri", "rect2sq", "hex6tri", "tri4tri", "rect3sq", "sq4tri", "tri2tri", "sq4sq", "rect4sq", "rect2tri"]:
        w, part, n, polys = FIG[key]
        q = fig(poly_svg(polys, "%d pieces" % n, gap=0.35)) + \
            "These pieces fit together to make one big shape. How many pieces are there?"
        e = "Count each piece: %s. There are <b>%d</b> pieces. Together they make a %s." % (
            ", ".join(str(k) for k in range(1, n + 1)), n, w)
        its.append(mcq(q, n, [n + 1, n - 1, n + 2, 2 * n], e))
    o = its
    order = [o[0], o[10], o[1], o[16], o[8], o[11], o[2], o[14], o[9], o[19],
             o[3], o[17], o[4], o[12], o[5], o[13], o[6], o[15], o[7], o[18]]
    assert len({id(x) for x in order}) == 20
    return {"title": "How many pieces?", "items": order}


# ============================================================ set 4: what big shape?
def set_big(rnd, K):
    its = []
    keys = ["sq2tri", "rect2sq", "rect2tri", "hex6tri", "tri2tri", "sq4sq", "rect3sq", "sq2rect", "tri4tri", "sq4tri"]
    for key in keys:
        w, part, n, polys = FIG[key]
        q = fig(poly_svg(polys, "%d pieces" % n, gap=0.35)) + "Push these %d %ss together. What big shape do they make?" % (n, part)
        e = "Slide the pieces together with no gaps. They make a <b>%s</b>." % w
        its.append(mcq(q, cap(w), [cap(x) for x in ["square", "rectangle", "triangle", "hexagon", "circle"] if x != w], e))
    for key in keys:
        w, part, n, _ = FIG[key]
        q = fig(whole_svg(key)) + "What is the name of the big shape?"
        e = "Look at the outside line only. It is a <b>%s</b>." % w
        its.append(mcq(q, cap(w), [cap(x) for x in ["square", "rectangle", "triangle", "hexagon", "circle"] if x != w], e))
    o = its
    order = [o[0], o[10], o[1], o[11], o[4], o[14], o[2], o[12], o[7], o[17],
             o[5], o[15], o[6], o[16], o[3], o[13], o[8], o[18], o[9], o[19]]
    return {"title": "What big shape?", "items": order}


# ============================================================ set 5: stories
def set_stories(rnd, K):
    its = []

    def s(key, text, ans, wr, e, gap=0.35):
        p = K.next()
        w, part, n, polys = FIG[key]
        its.append(mcq(fig(poly_svg(polys, "pieces", gap=gap)) + text.format(**p), ans, wr, e))

    sq = ["Square", "Rectangle", "Triangle", "Hexagon", "Circle"]
    s("rect2sq", "{n} puts 2 squares side by side. What shape does {he} make?", "Rectangle",
      [x for x in sq if x != "Rectangle"], "Two squares side by side make a long shape: a <b>rectangle</b>.")
    s("sq2tri", "{n} puts 2 triangles together. What shape does {he} make?", "Square",
      [x for x in sq if x != "Square"], "The two long sides match up. They make a <b>square</b>.")
    s("hex6tri", "{n} puts 6 triangles around a point. What shape does {he} make?", "Hexagon",
      [x for x in sq if x != "Hexagon"], "6 triangles around one point make a <b>hexagon</b>.")
    s("sq4sq", "{n} puts 4 small squares together in 2 rows. What shape does {he} make?", "Square",
      [x for x in sq if x != "Square"], "2 rows of 2 squares make a big <b>square</b>.")
    s("rect3sq", "{n} puts 3 squares in a row. What shape does {he} make?", "Rectangle",
      [x for x in sq if x != "Rectangle"], "3 squares in a row make a long <b>rectangle</b>.")
    s("tri4tri", "{n} puts 4 small triangles together. What shape does {he} make?", "Triangle",
      [x for x in sq if x != "Triangle"], "The 4 small triangles make one big <b>triangle</b>.")
    s("sq2rect", "{n} puts 2 rectangles together, one on top of the other. What shape does {he} make?", "Square",
      [x for x in sq if x != "Square"], "Two long rectangles stacked make a <b>square</b>.")
    s("rect2tri", "{n} puts 2 long triangles together. What shape does {he} make?", "Rectangle",
      [x for x in sq if x != "Rectangle"], "The long sides match up. They make a <b>rectangle</b>.")
    for key, text, ans, wr, e in [
        ("hex6tri", "{n} wants to make a hexagon with triangles. How many triangles does {he} need?", 6, [5, 3, 4],
         "6 triangles fit around one point to make a hexagon. The answer is <b>6</b>."),
        ("rect2sq", "{n} wants to make this rectangle with squares. How many squares does {he} need?", 2, [3, 4, 1],
         "The rectangle is 2 squares long. The answer is <b>2</b>."),
        ("sq4sq", "{n} wants to make a big square with small squares. How many small squares does {he} need?", 4, [2, 3, 6],
         "2 rows of 2 small squares: 2 + 2 = <b>4</b>."),
        ("sq2tri", "{n} cuts a square from corner to corner. How many triangles does {he} get?", 2, [4, 1, 3],
         "One cut from corner to corner makes <b>2</b> triangles."),
        ("tri4tri", "{n} wants to make a big triangle from small triangles. How many does {he} need?", 4, [3, 2, 6],
         "3 small triangles point up and 1 points down in the middle. That is <b>4</b>."),
        ("rect4sq", "{n} makes a long rectangle with squares. How many squares does {he} use?", 4, [3, 5, 2],
         "Count the squares in the row: 1, 2, 3, 4. The answer is <b>4</b>."),
    ]:
        p = K.next()
        its.append(mcq(fig(whole_svg(key)) + text.format(**p), ans, wr, e))
    for q, ans, wr, e in [
        ("A house picture is a square with a triangle on top. Which shapes do you need?", "A square and a triangle",
         ["2 squares", "2 triangles", "A circle and a square"], "The walls are a square and the roof is a triangle. <b>A square and a triangle</b>."),
        ("Which 2 shapes can make a square?", "2 triangles", ["2 circles", "2 hexagons", "1 circle and 1 triangle"],
         "Two triangles with their long sides together make a square. The answer is <b>2 triangles</b>."),
        ("Which 2 shapes can make a rectangle?", "2 squares", ["2 circles", "2 hexagons", "1 circle and 1 square"],
         "Two squares side by side make a rectangle. The answer is <b>2 squares</b>."),
        ("Can 2 circles fit together to make a square?", "No, circles are round and leave gaps",
         ["Yes, always", "Yes, if they are big", "Yes, if they are red"],
         "Circles have no straight sides. <b>No, circles are round and leave gaps</b>."),
        ("Can you take a square apart into 4 triangles?", "Yes, cut on both lines from corner to corner",
         ["No, never", "Yes, with 1 cut", "No, only into circles"],
         "Two cuts from corner to corner make 4 triangles. <b>Yes, cut on both lines from corner to corner</b>."),
        ("A rectangle is cut into 2 squares. Is it still the same amount of paper?", "Yes, the pieces make the same rectangle",
         ["No, it is more", "No, it is less", "We cannot tell"],
         "Cutting does not add or lose paper. <b>Yes, the pieces make the same rectangle</b>."),
    ]:
        pic = ""
        if q.startswith("A house"):
            pic = poly_svg([[(0, 2), (3, 2), (3, 5), (0, 5)], [(-0.4, 2), (1.5, 0.3), (3.4, 2)]], "a house made of a square and a triangle")
        its.append(mcq((fig(pic) if pic else "") + q, ans, wr, e))
    o = its
    order = [o[0], o[1], o[8], o[9], o[14], o[2], o[11], o[3], o[10], o[15],
             o[4], o[13], o[5], o[16], o[6], o[12], o[17], o[7], o[18], o[19]]
    assert len({id(x) for x in order}) == 20
    return {"title": "Putting shapes together", "items": order}


# ============================================================ lesson
def body_html():
    return (
        "<h2>Build shapes with sticks and clay</h2>"
        "<p>Each <b>stick</b> is a side. Each <b>clay ball</b> is a corner.</p>"
        "<figure class='sn-fig'>" + sticks_svg("triangle") + "<figcaption>3 sticks and 3 clay balls make a triangle.</figcaption></figure>"
        + table(["Shape", "Sticks", "Clay balls"], [["Triangle", "3", "3"], ["Square", "4", "4"], ["Rectangle", "4", "4"],
                                                    ["Hexagon", "6", "6"]]) +
        "<h2>Put small shapes together</h2>"
        "<p>Small shapes can fit together, with no gaps, to make a bigger shape.</p>"
        "<figure class='sn-fig'>" + whole_svg("sq2tri") + "<figcaption>2 triangles make a square.</figcaption></figure>"
        "<figure class='sn-fig'>" + whole_svg("rect2sq") + "<figcaption>2 squares make a rectangle.</figcaption></figure>"
        "<figure class='sn-fig'>" + whole_svg("hex6tri") + "<figcaption>6 triangles make a hexagon.</figcaption></figure>"
        "<h2>Common mistakes</h2>"
        + table(["Mistake", "What to do"], [
            ["Naming the pieces instead of the big shape", "Look at the outside line for the big shape"],
            ["Counting a piece twice", "Touch each piece once"],
            ["Leaving gaps between pieces", "Slide the sides together so they touch"],
        ])
    )


FAQ = [
    {"q": "What does compose shapes mean?",
     "a": "It means putting small shapes together to make a bigger shape. For example, 2 triangles can make a square and 2 squares can make a rectangle."},
    {"q": "Why do kindergartners build shapes with sticks and clay?",
     "a": "Building a shape shows its parts. Each stick is a side and each clay ball is a corner, so children learn why a triangle has 3 sides and 3 corners."},
    {"q": "How can I practice at home?",
     "a": "Use toothpicks and play dough, or cut paper squares into triangles and put them back together. Pattern blocks and tangrams are great too."},
    {"q": "How does this help later in math?",
     "a": "Seeing shapes made of smaller shapes helps with fractions (halves and fourths) and area in later grades."},
]


def gen():
    rnd = random.Random(2015)
    K = Kids(rnd)
    sets = [set_sticks(rnd, K), set_parts(rnd, K), set_count(rnd, K), set_big(rnd, K), set_stories(rnd, K)]
    finish(sets, rnd, max_num=12)
    return {
        "slug": "build-and-compose-shapes", "sort": 15, "updated": UPDATED, "pdf_url": "",
        "title": "Build and Compose Shapes: Put Shapes Together",
        "seo_title": "Kindergarten Composing Shapes Worksheets: Build Shapes and Make Bigger Shapes",
        "short_title": "Build and Compose Shapes",
        "domain": "Geometry",
        "standard_code": "K.G.B.6",
        "standard_url": "https://www.thecorestandards.org/Math/Content/K/G/B/6/",
        "standard_text": "Compose simple shapes to form larger shapes. For example, “Can you join these two triangles "
                         "with full sides touching to make a rectangle?”",
        "meta_desc": "Free kindergarten worksheets on composing shapes: build shapes with sticks and clay balls, find the "
                     "small shapes inside a big shape, count the pieces, and put triangles and squares together to make "
                     "squares, rectangles and hexagons. 100 picture questions with an answer key.",
        "key_big": "Small shapes can fit together to make a bigger shape.",
        "key_sub": "2 triangles make a square, 2 squares make a rectangle, 6 triangles make a hexagon.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }


if __name__ == "__main__":
    write_unit("us", "math", "kindergarten", gen())
