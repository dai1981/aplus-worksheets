# -*- coding: utf-8 -*-
"""India Class 2 Maths, Joyful Mathematics Chapter 5: Playing with Lines (Orientation of a Line)
Straight and curved lines; standing (vertical), sleeping (horizontal) and slanting lines; counting lines in shapes; parallel
lines (own makers with drawings, AU Year 2 set makers)."""
from in_prim import unit, mod, rn, co, mcq
from ws_common import svg_wrap, text, fig
au = mod("gen_au_maths_y2_shapes", 602051)

KINDS = {"standing": "vertical", "sleeping": "horizontal", "slanting": "slanting"}


def seg(kind, x, y, r):
    if kind == "standing":
        return (x, y - 32, x, y + 32)
    if kind == "sleeping":
        return (x - 34, y, x + 34, y)
    s = r.choice([1, -1])
    return (x - 26, y - 26 * s, x + 26, y + 26 * s)


def panel(kinds, r, curved=None):
    b = ""
    for i, k in enumerate(kinds):
        x = 50 + i * 100
        b += "<rect x='%d' y='8' width='90' height='90' rx='6' fill='none' stroke='#bbb'/>" % (x - 45)
        if k == "curved":
            b += "<path d='M%d 75 Q %d 10 %d 75' fill='none' stroke='#1f6f43' stroke-width='4'/>" % (x - 30, x, x + 30)
        elif k == "wavy":
            b += "<path d='M%d 53 q 15 -25 30 0 t 30 0' fill='none' stroke='#1f6f43' stroke-width='4'/>" % (x - 30)
        else:
            x1, y1, x2, y2 = seg(k, x, 53, r)
            b += "<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='#1f6f43' stroke-width='4'/>" % (x1, y1, x2, y2)
        b += text(x, 118, "ABCD"[i], 15)
    return svg_wrap(400, 128, b, "Four lines labelled A to D")


def one_line(r):
    want = r.choice(["standing", "sleeping", "slanting", "curved"])
    others = [k for k in ["standing", "sleeping", "slanting", "curved", "wavy"] if k != want and not (want == "curved" and k == "wavy")]
    ks = r.sample(others, 3)
    pos = r.randrange(4)
    ks.insert(pos, want)
    word = {"standing": "a standing (vertical) line", "sleeping": "a sleeping (horizontal) line", "slanting": "a slanting line", "curved": "a curved line"}[want]
    it = mcq(fig(panel(ks, r)) + "Which box shows %s?" % word, "ABCD"[pos], [c for c in "ABCD" if c != "ABCD"[pos]],
             "Box <b>%s</b> shows %s." % ("ABCD"[pos], word))
    return it


SHAPES = [("triangle", 3), ("square", 4), ("rectangle", 4), ("pentagon", 5), ("hexagon", 6)]


def poly_svg(n, r):
    import math
    pts = []
    rot = r.choice([0, 15, 30, 45])
    for i in range(n):
        a = math.radians(rot - 90 + 360 * i / n)
        pts.append("%.1f,%.1f" % (80 + 55 * math.cos(a), 70 + 55 * math.sin(a)))
    return svg_wrap(160, 140, "<polygon points='%s' fill='#eaf5ee' stroke='#1f6f43' stroke-width='3'/>" % " ".join(pts), "A shape made of straight lines")


def one_count(r):
    kind = r.choice(["poly", "poly", "letter", "letter"])
    if kind == "poly":
        n = r.choice([3, 4, 5, 6, 7, 8])
        return mcq(fig(poly_svg(n, r)) + "How many straight lines make this shape?", n, [n + 1, n - 1, n * 2], "Count the sides: <b>%d</b>." % n)
    L = {"L": 2, "T": 2, "H": 3, "E": 4, "F": 3, "I": 3, "N": 3, "Z": 3, "K": 3, "A": 3, "M": 4, "W": 4, "V": 2, "X": 2, "Y": 3}
    c = r.choice(sorted(L))
    n = L[c]
    return mcq("How many straight lines are needed to write the capital letter <b>%s</b> (in a plain style, with crossbars)?" % c, n, [n + 1, n - 1 if n > 2 else n + 2, n + 2],
               "Draw it: <b>%s</b> uses %d straight lines." % (c, n))


def one_where(r):
    t = r.choice([("The edge of a door from top to bottom is a ___ line.", "standing (vertical)"),
                  ("The top of a table is a ___ line when you look at it from the side.", "sleeping (horizontal)"),
                  ("A slide in the park makes a ___ line.", "slanting"), ("The edge of a bangle makes a ___ line.", "curved"),
                  ("A flagpole makes a ___ line.", "standing (vertical)"), ("The horizon over the sea looks like a ___ line.", "sleeping (horizontal)"),
                  ("A ladder leaning on a wall makes a ___ line.", "slanting"), ("A rainbow makes a ___ line.", "curved"),
                  ("A railway track on flat ground looks like ___ lines.", "sleeping (horizontal)"), ("The trunk of a coconut tree is close to a ___ line.", "standing (vertical)"),
                  ("The edge of a roti makes a ___ line.", "curved"), ("A kite string pulled up into the sky makes a ___ line.", "slanting")])
    q, a = t
    al = ["standing (vertical)", "sleeping (horizontal)", "slanting", "curved"]
    return mcq(q, a, [x for x in al if x != a], "<b>%s</b>." % a.capitalize())


unit(2, "playing-with-lines", 5, "G", 5, "Playing with Lines", "Straight, Curved, Standing, Sleeping and Slanting Lines", "lines",
     "Orientation of lines: straight and curved lines; vertical (standing), horizontal (sleeping) and slanting lines in the surroundings and in drawings (summary of NCERT Joyful Mathematics Class 2)",
     "Class 2 Playing with Lines worksheet (Joyful Mathematics Chapter 5): straight and curved lines, standing, sleeping and slanting lines, lines in shapes and letters. 100 picture questions with answers.",
     "Standing | sleeping — slanting /", "Curved lines bend; straight lines do not.",
     "<ul><li>A <b>standing</b> (vertical) line goes straight up and down.</li><li>A <b>sleeping</b> (horizontal) line goes side to side.</li><li>A <b>slanting</b> line leans. A <b>curved</b> line bends.</li></ul>",
     [("What kind of line is the edge of a wall going up?", ["It goes straight up"], "Standing (vertical)")],
     [["Calling a slanting line standing", "A standing line goes straight up, like a flagpole."], ["Counting a curve as straight", "A straight line does not bend at all."]],
     [("What is a horizontal line?", "A sleeping line that goes from side to side, like the top of a table."), ("What is a vertical line?", "A standing line that goes up and down, like a pole.")],
     [("Which line is it?", [co(one_line, 20)]),
      ("Lines around us", [co(one_where, 12), rn(au, "set_curved", 8)]),
      ("Straight lines in shapes", [co(one_count, 20)]),
      ("More lines", [co(one_line, 14), co(one_where, 0) if False else co(one_count, 6)]),
      ("Parallel lines", [rn(au, "set_parallel", 6), co(one_line, 14)])], 60205)
