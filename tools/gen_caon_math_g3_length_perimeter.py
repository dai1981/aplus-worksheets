# -*- coding: utf-8 -*-
"""
CA Grade 3 Math: Length and Perimeter (Ontario Mathematics Curriculum 2020, Spatial Sense E2.1, E2.2, E2.3)
  python3 tools/gen_ca_math_g3_length_perimeter.py
HTML attributes use single quotes (no backslashes in the JSON).
Canadian English (centimetre, metre, kilometre, colour), metric units only. 4-digit numbers have no separator.
Every length answer is parsed back to millimetres and checked in code; perimeters are computed from the sides.
Wrong answers come from real mistakes: a unit that does not fit the size, starting at 1 or reading the end number
when the object does not start at 0, counting marks instead of spaces, adding only the two numbers shown on a
rectangle, leaving out a side, giving the area instead of the perimeter, and forgetting to halve for a width.
"""
import json, math, os, random, re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "ca-on", "math", "grade-3")
UPDATED = "2026-11-02"
GREEN = "#006633"
FILL = "#cfe6d6"
RED = "#c0392b"
INK = "#2b2b2b"
WOOD = "#f6e7b8"
FONT = "Arial, Helvetica, sans-serif"
NBSP = " "


# ------------------------------------------------------------ units and checking
UNIT = {"mm": 1, "cm": 10, "m": 1000, "km": 1000000}
TOK = re.compile(r"([\d" + NBSP + r"]+)\s*(km|mm|cm|m)(?![a-zA-Z])")


def parse(s):
    """'1 m' -> 1000 (mm). None if the string is not a plain length."""
    s = s.strip()
    pos, tot, hit = 0, 0, False
    for mt in TOK.finditer(s):
        if s[pos:mt.start()].strip():
            return None
        tot += int(mt.group(1).replace(NBSP, "")) * UNIT[mt.group(2)]
        pos, hit = mt.end(), True
    if not hit or s[pos:].strip():
        return None
    return tot


def c(n):
    """Ontario style: 4 digits plain (1000), 5 or more digits grouped with a no-break space."""
    if n < 10000:
        return str(n)
    return "{:,}".format(n).replace(",", NBSP)


def L(v, u):
    return "%s %s" % (c(v), u)


# ------------------------------------------------------------ helpers
def mcq(q, correct, cands, e, rnd, want=None):
    """4 choices: correct + 3 unique distractors. Length choices must all differ in value.
    want = value in mm checks the correct answer."""
    correct = str(correct)
    if want is not None:
        assert parse(correct) == want, (q, correct, want, parse(correct))
    seen = {correct}
    pc = parse(correct)
    vals = {pc} if pc is not None else set()
    pick = []
    for x in cands:
        x = str(x)
        lead = x.split(" ")[0]
        if x in seen or not x or lead.startswith("-") or lead.startswith("−") or lead == "0":
            continue
        pv = parse(x)
        if pv is not None:
            if pv in vals:
                continue
            vals.add(pv)
        seen.add(x)
        pick.append(x)
        if len(pick) == 3:
            break
    assert len(pick) == 3, (q, correct, cands)
    ch = pick + [correct]
    rnd.shuffle(ch)
    return {"q": q, "c": ch, "a": ch.index(correct), "e": e}


def fig(svg):
    return "<div class='qfig'>" + svg + "</div>"


def svg_wrap(w, h, body, label):
    return ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 %d %d' width='%d' height='%d' "
            "role='img' aria-label='%s'><g font-family='%s'>%s</g></svg>" % (w, h, w, h, label, FONT, body))


def text(x, y, t, fs=17, anchor="middle", bold=True, col=INK):
    return ("<text x='%.1f' y='%.1f' font-size='%d'%s fill='%s' text-anchor='%s'>%s</text>"
            % (x, y, fs, " font-weight='700'" if bold else "", col, anchor, t))


def plus(nums):
    return " + ".join(str(n) for n in nums)


def cap(s):
    return s[0].upper() + s[1:]


# ------------------------------------------------------------ ruler figure
def draw_object(kind, a, b):
    """An object lying exactly from x=a to x=b, between y=12 and y=32."""
    o = []
    if kind in ("pencil", "crayon"):
        body = "#f4c542" if kind == "pencil" else "#3a6fb0"
        tipc = WOOD if kind == "pencil" else body
        tip = min(22, (b - a) * 0.3)
        o.append("<rect x='%.1f' y='12' width='%.1f' height='20' fill='%s' stroke='%s' stroke-width='1.5'/>"
                 % (a, b - a - tip, body, INK))
        if kind == "pencil":
            o.append("<rect x='%.1f' y='12' width='8' height='20' fill='#e98aa0' stroke='%s' stroke-width='1.5'/>" % (a, INK))
        else:
            o.append("<rect x='%.1f' y='12' width='%.1f' height='20' fill='#fff' stroke='%s' stroke-width='1.5'/>"
                     % (a + (b - a - tip) * 0.25, (b - a - tip) * 0.4, INK))
        o.append("<path d='M%.1f 12 L%.1f 22 L%.1f 32 Z' fill='%s' stroke='%s' stroke-width='1.5' stroke-linejoin='round'/>"
                 % (b - tip, b, b - tip, tipc, INK))
        if kind == "pencil":
            o.append("<path d='M%.1f 19.5 L%.1f 22 L%.1f 24.5 Z' fill='%s'/>" % (b - tip * 0.25, b, b - tip * 0.25, INK))
    elif kind == "eraser":
        o.append("<rect x='%.1f' y='12' width='%.1f' height='20' rx='4' fill='#f7b7c5' stroke='%s' stroke-width='1.5'/>"
                 % (a, b - a, INK))
        o.append("<rect x='%.1f' y='12' width='%.1f' height='20' fill='#5dade2' stroke='%s' stroke-width='1.5'/>"
                 % (a + (b - a) * 0.45, (b - a) * 0.4, INK))
    elif kind == "stick":   # hockey stick key chain: a small stick shape
        blade = min(16, (b - a) * 0.3)
        o.append("<rect x='%.1f' y='14' width='%.1f' height='9' fill='#c98a4b' stroke='%s' stroke-width='1.5'/>"
                 % (a, b - a - blade + 2, INK))
        o.append("<path d='M%.1f 14 L%.1f 14 L%.1f 32 L%.1f 32 Z' fill='#2b2b2b' stroke='%s' stroke-width='1.5' "
                 "stroke-linejoin='round'/>" % (b - blade, b - blade + 6, b, b - blade - 2, INK))
        o.append("<path d='M%.1f 32 L%.1f 32 L%.1f 24 Z' fill='#2b2b2b' stroke='%s' stroke-width='1.5' stroke-linejoin='round'/>"
                 % (b - blade - 2, b, b, INK))
    else:  # ribbon
        o.append("<rect x='%.1f' y='15' width='%.1f' height='14' fill='%s' stroke='%s' stroke-width='1.5'/>"
                 % (a, b - a, RED, INK))
    return "".join(o)


NAMES = {"pencil": "pencil", "crayon": "crayon", "eraser": "eraser", "ribbon": "piece of ribbon",
         "stick": "toy hockey stick"}


def ruler_svg(s_mm, e_mm, kind="pencil", ncm=None):
    """Ruler from 0 to ncm cm with mm marks and an object from s_mm to e_mm (exact)."""
    if ncm is None:
        ncm = max(8, -(-e_mm // 10) + 1)
    PX = 38.0
    X0, YR, RH = 18, 40, 50
    W = int(X0 * 2 + PX * ncm + 26)
    H = YR + RH + 4
    X = lambda mm: X0 + PX * mm / 10.0
    a, b = X(s_mm), X(e_mm)
    o = [draw_object(kind, a, b)]
    for x in (a, b):
        o.append("<line x1='%.1f' y1='32' x2='%.1f' y2='%d' stroke='%s' stroke-width='1.2' stroke-dasharray='3 2'/>"
                 % (x, x, YR, RED))
    o.append("<rect x='4' y='%d' width='%d' height='%d' rx='3' fill='%s' stroke='%s' stroke-width='2'/>"
             % (YR, W - 8, RH, WOOD, INK))
    small, big = [], []
    for i in range(ncm * 10 + 1):
        x = X(i)
        ln = 18 if i % 10 == 0 else (12 if i % 5 == 0 else 7)
        (big if i % 10 == 0 else small).append("M%.1f %dL%.1f %d" % (x, YR, x, YR + ln))
    o.append("<path d='%s' stroke='%s' stroke-width='1'/>" % ("".join(small), INK))
    o.append("<path d='%s' stroke='%s' stroke-width='2'/>" % ("".join(big), INK))
    for cc in range(ncm + 1):
        o.append(text(X(cc * 10), YR + 38, str(cc), 15))
    o.append(text(X(ncm * 10) + 12, YR + 38, "cm", 15, anchor="start", bold=False))
    art = "an" if kind == "eraser" else "a"
    return svg_wrap(W, H, "".join(o), "ruler with %s %s from %d mm to %d mm" % (art, NAMES[kind], s_mm, e_mm))


# ------------------------------------------------------------ polygon and grid figures
def polygon_svg(pts, labels, label="polygon with side lengths"):
    """Polygon (pixel points) with a label outside the middle of each side. A label of '' is not drawn;
    a label containing '?' is drawn in red. The picture is sized to fit the labels."""
    CW, TH = 9.6, 13
    cx = sum(p[0] for p in pts) / len(pts)
    cy = sum(p[1] for p in pts) / len(pts)
    n = len(pts)
    texts = []
    for i in range(n):
        t = labels[i]
        if not t:
            continue
        (x1, y1), (x2, y2) = pts[i], pts[(i + 1) % n]
        mx, my = (x1 + x2) / 2, (y1 + y2) / 2
        dx, dy = x2 - x1, y2 - y1
        Ln = math.hypot(dx, dy) or 1
        nx, ny = -dy / Ln, dx / Ln
        if (mx + nx - cx) ** 2 + (my + ny - cy) ** 2 < (mx - cx) ** 2 + (my - cy) ** 2:
            nx, ny = -nx, -ny
        hw = CW * len(t) / 2
        off = 7 + abs(nx) * hw + abs(ny) * TH
        texts.append((mx + nx * off, my + ny * off, hw, t))
    xs = [p[0] for p in pts] + [x - hw for x, y, hw, t in texts] + [x + hw for x, y, hw, t in texts]
    ys = [p[1] for p in pts] + [y - TH for x, y, hw, t in texts] + [y + TH for x, y, hw, t in texts]
    pad = 6
    ox, oy = min(xs) - pad, min(ys) - pad
    W, H = int(max(xs) - ox + pad), int(max(ys) - oy + pad)
    s = ["<polygon points='%s' fill='%s' stroke='%s' stroke-width='3' stroke-linejoin='round'/>"
         % (" ".join("%.0f,%.0f" % (x - ox, y - oy) for x, y in pts), FILL, GREEN)]
    for x, y, hw, t in texts:
        col = RED if "?" in t else INK
        s.append(text(x - ox, y - oy + 6, t, 17, col=col))
    return svg_wrap(W, H, "".join(s), label)


def grid_svg(cells_w, cells_h, filled, cell=28, label="shape on a grid"):
    """Grid of cells_w x cells_h squares; `filled` is a set of (col, row) squares that make the shape.
    The outline of the shape is drawn thick so the sides can be counted."""
    W, H = cells_w * cell + 20, cells_h * cell + 20
    s = []
    for (cc, r) in sorted(filled):
        s.append("<rect x='%d' y='%d' width='%d' height='%d' fill='%s' stroke='%s' stroke-width='1'/>"
                 % (10 + cc * cell, 10 + r * cell, cell, cell, FILL, GREEN))
    for (cc, r) in sorted(filled):
        x, y = 10 + cc * cell, 10 + r * cell
        for (dc, dr, x1, y1, x2, y2) in [(0, -1, x, y, x + cell, y), (0, 1, x, y + cell, x + cell, y + cell),
                                          (-1, 0, x, y, x, y + cell), (1, 0, x + cell, y, x + cell, y + cell)]:
            if (cc + dc, r + dr) not in filled:
                s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='3.5' stroke-linecap='round'/>"
                         % (x1, y1, x2, y2, GREEN))
    return svg_wrap(W, H, "".join(s), label)


def edges(filled):
    n = 0
    for (cc, r) in filled:
        for (dc, dr) in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
            if (cc + dc, r + dr) not in filled:
                n += 1
    return n


def rect_cells(w, h, c0=0, r0=0):
    return {(c0 + i, r0 + j) for i in range(w) for j in range(h)}


def rect_pts(Lg, Wd, max_w=200, max_h=100):
    k = min(max_w / Lg, max_h / Wd, 26)
    return [(0, 0), (Lg * k, 0), (Lg * k, Wd * k), (0, Wd * k)]


QUAD = [[(0, 0), (150, 0), (200, 110), (20, 110)], [(30, 0), (170, 20), (200, 120), (0, 100)],
        [(0, 20), (120, 0), (190, 90), (60, 120)]]
PENT = [[(100, 0), (200, 60), (165, 140), (35, 140), (0, 60)], [(0, 50), (90, 0), (190, 30), (170, 130), (20, 130)]]
HOUSE = [(0, 50), (90, 0), (180, 50), (180, 140), (0, 140)]


def reg_pts(n, r=62):
    return [(r + r * math.cos(2 * math.pi * i / n - math.pi / 2), r + r * math.sin(2 * math.pi * i / n - math.pi / 2))
            for i in range(n)]


SHAPE_NAME = {3: "triangle", 4: "quadrilateral", 5: "pentagon", 6: "hexagon", 8: "octagon"}


def tri_pts(a, b, cc, size=190):
    """Triangle drawn to scale: base cc, right side a, left side b. Sides in order: left (b), right (a), base (cc)."""
    k = size / max(a, b, cc)
    A, B, C = a * k, b * k, cc * k
    x = (B * B - A * A + C * C) / (2 * C)
    y = math.sqrt(max(B * B - x * x, 1))
    return [(0, y), (x, 0), (C, y)]


def tri_shape(rnd, lo=3, hi=12):
    while True:
        a, b, cc = rnd.randint(lo, hi), rnd.randint(lo, hi), rnd.randint(lo + 1, hi + 2)
        x, y, z = sorted([a, b, cc])
        if x + y > z + 1 and len({a, b, cc}) >= 2:
            break
    a, b = (x, y) if rnd.random() < 0.5 else (y, x)
    return tri_pts(a, b, z), [b, a, z]


def scaled_sides(pts, rnd, lo=2, hi=15):
    """Integer side lengths in proportion to a template, so the picture matches the numbers."""
    n = len(pts)
    lens = [math.hypot(pts[(i + 1) % n][0] - pts[i][0], pts[(i + 1) % n][1] - pts[i][1]) for i in range(n)]
    for _ in range(50):
        unit = max(lens) / rnd.randint(max(lo + 3, 6), hi)
        sides = [max(lo, int(round(v / unit))) for v in lens]
        if max(sides) <= hi:
            return sides
    return sides


def curved_svg():
    """A flat shape with one straight side and one curved side (a half circle), for the string question."""
    r = 70
    body = ("<path d='M10 %d L%d %d A%d %d 0 0 0 10 %d Z' fill='%s' stroke='%s' stroke-width='3'/>"
            % (r + 10, 2 * r + 10, r + 10, r, r, r + 10, FILL, GREEN))
    return svg_wrap(2 * r + 20, r + 20, body, "half circle with one curved side")


# ------------------------------------------------------------ set 1: units and benchmarks
def set_units(rnd):
    its = []
    for obj, ans, wr, e in [
        ("the length of a ladybug", "mm", ["km", "m", "L"],
         "A ladybug is tiny, smaller than your fingernail, so use millimetres."),
        ("the length of a crayon", "cm", ["km", "m", "kg"],
         "A crayon fits on a ruler, so use centimetres. Kilograms measure mass, not length."),
        ("the length of a hockey rink", "m", ["mm", "km", "kg"],
         "You can skate from one end of a rink to the other in a few seconds, so use metres."),
        ("the distance from Toronto to Ottawa", "km", ["m", "cm", "mm"],
         "Toronto to Ottawa is a long drive of a few hours, so use kilometres."),
        ("how thick a loonie is", "mm", ["cm", "m", "km"],
         "A loonie is very thin, about 2 mm thick, so use millimetres."),
        ("the height of the classroom door", "m", ["km", "mm", "L"],
         "A door is a bit taller than an adult, about 2 m. Litres measure how much a container holds."),
        ("the length of the Terry Fox Run route", "km", ["mm", "cm", "kg"],
         "The Terry Fox Run is a long walk or run, so use kilometres."),
        ("the width of your math notebook", "cm", ["km", "m", "L"],
         "A notebook fits on your desk and on a 30 cm ruler, so use centimetres."),
    ]:
        its.append(mcq("Which unit is best to measure %s?" % obj, ans, wr, e, rnd))
    its.append(mcq("How many millimetres are in 1 centimetre?", "10 mm", ["100 mm", "1 mm", "1000 mm"],
                   "Look at a ruler. There are 10 small spaces in each centimetre. So 1 cm = 10 mm.", rnd, want=10))
    its.append(mcq("How many centimetres are in 1 metre?", "100 cm", ["10 cm", "1000 cm", "50 cm"],
                   "A metre stick has 100 centimetres marked on it. So 1 m = 100 cm.", rnd, want=1000))
    its.append(mcq("How many metres are in 1 kilometre?", "1000 m", ["100 m", "10 m", "1 m"],
                   "Kilo means 1000. So 1 km = 1000 m.", rnd, want=1000000))
    its.append(mcq("Which list goes from the <b>shortest</b> unit to the <b>longest</b> unit?", "mm, cm, m, km",
                   ["km, m, cm, mm", "cm, mm, m, km", "mm, m, cm, km"],
                   "A millimetre is the smallest. 10 mm make 1 cm, 100 cm make 1 m, and 1000 m make 1 km.", rnd))
    for q, ans, wr, e in [
        ("Your fingernail is about ☐ wide.", "1 cm", ["1 m", "1 mm", "1 km"],
         "The width of a fingernail is a good benchmark for 1 cm. 1 mm is about as thick as a dime."),
        ("A dime is about ☐ thick.", "1 mm", ["1 cm", "1 m", "10 cm"],
         "A dime is very thin. Its thickness is a good benchmark for 1 mm."),
        ("A classroom door is about ☐ tall.", "2 m", ["2 cm", "2 km", "20 m"],
         "A door is a bit taller than an adult. That is about 2 m. 2 cm is shorter than your finger."),
        ("A new pencil is about ☐ long.", "19 cm", ["19 m", "19 mm", "19 km"],
         "A new pencil fits on a 30 cm ruler, so it is about 19 cm. 19 mm is only about as long as a fingertip."),
        ("A Grade 3 student is about ☐ tall.", "130 cm", ["130 m", "13 cm", "13 m"],
         "Most Grade 3 students are between 1 m and 1 m 50 cm tall. 130 cm fits. 13 cm is the size of a hand."),
        ("A school bus is about ☐ long.", "12 m", ["12 cm", "12 km", "120 m"],
         "A school bus is about as long as 6 classroom doors lying end to end, so about 12 m."),
        ("You can walk about ☐ in 15 minutes.", "1 km", ["1 m", "1 cm", "100 km"],
         "A 15-minute walk is a good benchmark for 1 km. You can walk 1 m in one big step."),
    ]:
        its.append(mcq("Choose the best estimate. " + q, ans, wr, e, rnd))
    its.append(mcq("Which is about 1 m long?", "a metre stick, or a big step",
                   ["your fingernail", "a soccer field", "a trip to Ottawa"],
                   "1 m is the length of a metre stick, or about one big step for an adult. A fingernail is about 1 cm.",
                   rnd))
    assert len(its) == 20, len(its)
    return {"title": "Choose the unit and use benchmarks", "items": its}


# ------------------------------------------------------------ set 2: measure with a ruler
def set_ruler(rnd):
    its = []
    for e_cm, kind in [(7, "pencil"), (5, "crayon"), (4, "eraser"), (9, "ribbon")]:
        nm = NAMES[kind]
        q = fig(ruler_svg(0, e_cm * 10, kind)) + "How long is the %s?" % nm
        e = ("The %s starts at 0 and ends at %d. So it is %d cm long. Count the spaces between the numbers, "
             "not the marks: there are %d marks but only %d spaces." % (nm, e_cm, e_cm, e_cm + 1, e_cm))
        its.append(mcq(q, "%d cm" % e_cm, ["%d cm" % (e_cm + 1), "%d cm" % (e_cm - 1), "%d m" % e_cm], e, rnd,
                       want=e_cm * 10))
    for s_cm, e_cm, kind in [(2, 9, "pencil"), (1, 6, "crayon"), (3, 7, "eraser"), (2, 8, "ribbon"),
                             (3, 11, "pencil"), (4, 9, "stick")]:
        nm = NAMES[kind]
        ln = e_cm - s_cm
        q = fig(ruler_svg(s_cm * 10, e_cm * 10, kind)) + "How long is the %s?" % nm
        e = ("The %s starts at %d, not at 0. It ends at %d. %d − %d = %d, so it is %d cm long. "
             "You can also count the spaces from %d to %d: there are %d." % (nm, s_cm, e_cm, e_cm, s_cm, ln, ln,
                                                                            s_cm, e_cm, ln))
        its.append(mcq(q, "%d cm" % ln, ["%d cm" % e_cm, "%d cm" % (ln + 1), "%d cm" % (e_cm + s_cm),
                                         "%d cm" % (ln - 1)], e, rnd, want=ln * 10))
    for n, thing, he, e_cm in [("Owen", "his crayon", "he", 8), ("Hana", "her library card", "she", 10)]:
        ln = e_cm - 1
        its.append(mcq("%s puts one end of %s at 1 on the ruler, not at 0. The other end is at %d. "
                       "How long is it?" % (n, thing, e_cm), "%d cm" % ln,
                       ["%d cm" % e_cm, "%d cm" % (e_cm + 1), "%d cm" % (ln - 1)],
                       "%s started at 1, so the number at the end is 1 too big. %d − 1 = %d cm."
                       % (cap(he), e_cm, ln), rnd, want=ln * 10))
    for e_mm, kind in [(46, "crayon"), (63, "pencil"), (35, "eraser")]:
        nm = NAMES[kind]
        a, b = divmod(e_mm, 10)
        q = fig(ruler_svg(0, e_mm, kind)) + "How long is the %s in millimetres?" % nm
        e = ("The %s goes past %d cm and then %d small marks more. %d cm = %d mm, and %d + %d = %d. "
             "So it is %d mm long." % (nm, a, b, a, a * 10, a * 10, b, e_mm, e_mm))
        its.append(mcq(q, "%d mm" % e_mm, ["%d mm" % (a + b), "%d mm" % (a * 100 + b), "%d cm" % e_mm,
                                           "%d mm" % (e_mm + 10)], e, rnd, want=e_mm))
    its.append(mcq(fig(ruler_svg(20, 74, "pencil")) + "How long is the pencil in millimetres?", "54 mm",
                   ["74 mm", "64 mm", "54 cm"],
                   "The pencil starts at 2 cm, not at 0. It ends at 7 cm and 4 small marks, which is 74 mm. "
                   "2 cm = 20 mm. 74 − 20 = 54 mm.", rnd, want=54))
    its.append(mcq(fig(ruler_svg(30, 88, "crayon")) + "How long is the crayon in millimetres?", "58 mm",
                   ["88 mm", "68 mm", "58 cm"],
                   "The crayon starts at 3 cm = 30 mm. It ends at 8 cm and 8 small marks, which is 88 mm. "
                   "88 − 30 = 58 mm.", rnd, want=58))
    its.append(mcq("Leah measures a ribbon. It goes from 0 to 6 on the ruler. She counts the marks "
                   "0, 1, 2, 3, 4, 5, 6 and says the ribbon is 7 cm. How long is it really?", "6 cm",
                   ["7 cm", "5 cm", "60 cm"],
                   "Leah counted 7 marks, but length is the number of spaces between them. From 0 to 6 there are "
                   "6 spaces, so the ribbon is 6 cm.", rnd, want=60))
    its.append(mcq("Sofia’s marker lies on a ruler. One end is at the 4 cm mark and the other end is at the "
                   "12 cm mark. How long is the marker?", "8 cm", ["12 cm", "9 cm", "16 cm"],
                   "It does not start at 0, so subtract: 12 − 4 = 8 cm. 16 cm adds the numbers instead.", rnd,
                   want=80))
    its.append(mcq("A paper clip is 30 mm long. How many centimetres is that?", "3 cm",
                   ["300 cm", "30 cm", "13 cm"],
                   "10 mm = 1 cm. 30 mm is 3 groups of 10 mm, so it is 3 cm.", rnd, want=30))
    assert len(its) == 20, len(its)
    return {"title": "Measure with a ruler (not always from 0)", "items": its}


# ------------------------------------------------------------ set 3: perimeter by adding sides
def sum_cands(sides, total):
    """Typical slips: leaving out a side, counting a side twice, regrouping by 10."""
    return [total - max(sides), total - min(sides), total + min(sides), total + 10, total - 10, total + 1]


def set_add(rnd):
    its = []
    # grid shapes: count the unit sides (wrong: the area, length + width, off by a corner)
    for w, h in [(4, 2), (5, 3), (3, 3), (6, 2), (2, 5)]:
        p, a = 2 * (w + h), w * h
        shape = "square" if w == h else "rectangle"
        its.append(mcq(fig(grid_svg(w, h, rect_cells(w, h), label="%s %d by %d on a grid" % (shape, w, h))) +
                       "Each small square is 1 cm on each side. What is the perimeter of the %s?" % shape,
                       "%d cm" % p, ["%d cm" % v for v in [a, w + h, p - 2, p + 2, p + 4]],
                       "Count the 1 cm sides all the way around: %d + %d + %d + %d = %d cm. "
                       "%d is the number of squares inside. That is the area, not the perimeter."
                       % (w, h, w, h, p, a), rnd, want=p * 10))
    cells = rect_cells(2, 2) | rect_cells(5, 2, 0, 2)
    p = edges(cells)
    assert p == 2 * (5 + 4) and len(cells) == 14
    its.append(mcq(fig(grid_svg(5, 4, cells, label="L-shaped figure on a grid")) +
                   "Each small square is 1 cm on each side. What is the perimeter of the shape?",
                   "%d cm" % p, ["%d cm" % v for v in [len(cells), p - 2, p - 4, p + 2]],
                   "Go around the outside and count every 1 cm side, including the short step: %d cm. "
                   "There are %d squares inside, but that is the area." % (p, len(cells)), rnd, want=p * 10))
    # polygons with every side labelled
    plan = [("tri", "cm"), ("tri", "m"), ("quad", "cm"), ("quad", "m"), ("pent", "cm"), ("house", "m")]
    for kind, u in plan:
        if kind == "tri":
            pts, sides = tri_shape(rnd)
        elif kind == "quad":
            pts = rnd.choice(QUAD)
            sides = scaled_sides(pts, rnd)
        elif kind == "pent":
            pts = rnd.choice(PENT)
            sides = scaled_sides(pts, rnd, hi=12)
        else:
            pts = HOUSE
            sides = scaled_sides(pts, rnd, hi=12)
        p = sum(sides)
        name = SHAPE_NAME[len(sides)]
        lab = ["%d %s" % (v, u) for v in sides]
        its.append(mcq(fig(polygon_svg(pts, lab, "%s with side lengths" % name)) +
                       "What is the perimeter of this %s?" % name,
                       "%d %s" % (p, u), ["%d %s" % (v, u) for v in sum_cands(sides, p)],
                       "Add every side: %s = %d %s. Touch each side as you add it so you do not skip one."
                       % (plus(sides), p, u), rnd, want=p * UNIT[u]))
    # rectangles and squares that show only some sides
    for Lg, Wd, u in [(9, 4, "cm"), (12, 5, "m")]:
        p = 2 * (Lg + Wd)
        its.append(mcq(fig(polygon_svg(rect_pts(Lg, Wd), ["%d %s" % (Lg, u), "", "", "%d %s" % (Wd, u)],
                                       "rectangle %d by %d" % (Lg, Wd))) +
                       "What is the perimeter of the rectangle?", "%d %s" % (p, u),
                       ["%d %s" % v for v in [(Lg + Wd, u), (Lg * Wd, u), (2 * Lg + Wd, u)]],
                       "A rectangle has 2 long sides and 2 short sides: %d + %d + %d + %d = %d %s. "
                       "Adding only %d + %d = %d forgets the other two sides."
                       % (Lg, Wd, Lg, Wd, p, u, Lg, Wd, Lg + Wd), rnd, want=p * UNIT[u]))
    for s, u in [(6, "cm"), (8, "m")]:
        p = 4 * s
        its.append(mcq(fig(polygon_svg(rect_pts(s, s), ["%d %s" % (s, u), "", "", ""], "square")) +
                       "This is a square. What is its perimeter?", "%d %s" % (p, u),
                       ["%d %s" % (v, u) for v in [s, 2 * s, s * s, 3 * s]],
                       "A square has 4 equal sides: %d + %d + %d + %d = %d %s." % (s, s, s, s, p, u), rnd,
                       want=p * UNIT[u]))
    for n, s in [(6, 5), (8, 3)]:
        p = n * s
        its.append(mcq(fig(polygon_svg(reg_pts(n), ["%d cm" % s] + [""] * (n - 1), "%s with equal sides" % SHAPE_NAME[n])) +
                       "All the sides of this %s are the same length. What is its perimeter?" % SHAPE_NAME[n],
                       "%d cm" % p, ["%d cm" % v for v in [s, (n - 1) * s, n + s, 4 * s]],
                       "%s %s has %d sides. Add %d cm %d times: %s = %d cm." % ("An" if n == 8 else "A", SHAPE_NAME[n], n, s, n,
                                                                            plus([s] * n), p), rnd, want=p * 10))
    its.append(mcq(fig(curved_svg()) + "How can you measure the perimeter of a shape with a curved side?",
                   "Lay a string along the edge, then measure the string",
                   ["Count the squares inside the shape", "Measure only the straight side",
                    "Measure across the middle of the shape"],
                   "A ruler cannot bend around a curve. Lay a string all the way around the edge, mark where it "
                   "meets, then straighten the string and measure it with a ruler.", rnd))
    its.append(mcq("What is perimeter?", "the distance all the way around a shape",
                   ["the space inside a shape", "the length of the longest side", "the number of corners"],
                   "Perimeter is the distance around the outside edge. The space inside is the area.", rnd))
    assert len(its) == 20, len(its)
    return {"title": "Perimeter: add all the sides", "items": its}


# ------------------------------------------------------------ set 4: missing side and building shapes
def set_missing(rnd):
    its = []
    for i in range(8):
        u = ["cm", "m"][i % 2]
        if i % 2 == 0:
            pts, sides = tri_shape(rnd, 4, 14)
        else:
            pts = rnd.choice(QUAD)
            sides = scaled_sides(pts, rnd, hi=14)
        k = rnd.randrange(len(sides))
        p, x = sum(sides), sides[k]
        known = [v for j, v in enumerate(sides) if j != k]
        lab = ["%d %s" % (v, u) for v in sides]
        lab[k] = "? %s" % u
        name = SHAPE_NAME[len(sides)]
        its.append(mcq(fig(polygon_svg(pts, lab, "%s with one unknown side" % name)) +
                       "The perimeter of this %s is %d %s. What is the missing side length?" % (name, p, u),
                       "%d %s" % (x, u),
                       ["%d %s" % (v, u) for v in [sum(known), p + sum(known), x + 2, x - 2, x + 10, x + 1]],
                       "Add the sides you know: %s = %d. Then subtract from the perimeter: %d − %d = %d %s."
                       % (plus(known), sum(known), p, sum(known), x, u), rnd, want=x * UNIT[u]))
    for Lg, Wd, u in [(8, 3, "cm"), (10, 6, "m"), (7, 5, "cm"), (12, 4, "m"), (9, 2, "cm")]:
        p = 2 * (Lg + Wd)
        its.append(mcq("A rectangle has a perimeter of %d %s. It is %d %s long. How wide is it?" % (p, u, Lg, u),
                       "%d %s" % (Wd, u),
                       ["%d %s" % (v, u) for v in [p - Lg, p - 2 * Lg, p // 2, Wd + 1]],
                       "The two lengths use %d + %d = %d %s. That leaves %d − %d = %d %s for the two widths, "
                       "so each width is %d ÷ 2 = %d %s." % (Lg, Lg, 2 * Lg, u, p, 2 * Lg, 2 * Wd, u, 2 * Wd, Wd, u),
                       rnd, want=Wd * UNIT[u]))
    for s, u in [(5, "cm"), (9, "m"), (7, "cm")]:
        p = 4 * s
        its.append(mcq("A square has a perimeter of %d %s. How long is each side?" % (p, u), "%d %s" % (s, u),
                       ["%d %s" % (v, u) for v in [p // 2, p - 4, s + 2, s + 1]],
                       "A square has 4 equal sides. %d ÷ 4 = %d %s. Check: %s = %d." % (p, s, u, plus([s] * 4), p),
                       rnd, want=s * UNIT[u]))
    # build a rectangle with a given perimeter (wrong: area = P, length + width = P, one side off)
    for P, good, wrong in [(20, (6, 4), [(4, 5), (10, 10), (6, 5)]),
                           (16, (5, 3), [(2, 8), (8, 8), (5, 4)]),
                           (24, (8, 4), [(4, 6), (12, 12), (8, 5)]),
                           (18, (7, 2), [(2, 9), (9, 9), (7, 3)])]:
        a, b = good
        assert 2 * (a + b) == P
        for x, y in wrong:
            assert 2 * (x + y) != P
        cands = ["%d cm by %d cm" % w for w in wrong]
        e = ("%d + %d + %d + %d = %d cm. A quick check: length + width must be half of %d, which is %d. "
             "%s has an area of %d, not a perimeter of %d."
             % (a, b, a, b, P, P, P // 2, cands[0], wrong[0][0] * wrong[0][1], P))
        its.append(mcq("Which rectangle has a perimeter of %d cm?" % P, "%d cm by %d cm" % good, cands, e, rnd))
    assert len(its) == 20, len(its)
    return {"title": "Find the missing side and build a shape", "items": its}


# ------------------------------------------------------------ set 5: word problems
def set_story(rnd):
    its = []

    def add(q, r, w, e, want=None):
        its.append(mcq(q, r, w, e, rnd, want=want))

    add("Priya’s family has a vegetable garden that is 8 m long and 5 m wide. They want a fence all the way "
        "around it. How much fence do they need?", "26 m", ["13 m", "40 m", "21 m"],
        "The fence goes around all 4 sides: 8 + 5 + 8 + 5 = 26 m. 40 is the area, and 13 m is only two sides.",
        26000)
    add("A hockey rink is about 60 m long and 30 m wide. About how far is it all the way around the boards?",
        "180 m", ["90 m", "1800 m", "150 m"],
        "Add all 4 sides: 60 + 30 + 60 + 30 = 180 m. 90 m is only one length and one width.", 180000)
    add("For the Terry Fox Run, Grade 3 runs around the school field. The field is 150 m long and 100 m wide. "
        "How far is one lap?", "500 m", ["250 m", "400 m", "350 m"],
        "One lap goes around all 4 sides: 150 + 100 + 150 + 100 = 500 m. 400 m leaves out one short side.", 500000)
    add("One lap around that field is 500 m. How many laps make 1 km?", "2", ["5", "10", "3"],
        "1 km = 1000 m. 500 m + 500 m = 1000 m, so 2 laps make 1 km.")
    add("Zoe glues ribbon around the edge of a square picture frame. Each side is 25 cm. How much ribbon "
        "does she need?", "100 cm", ["50 cm", "75 cm", "625 cm"],
        "A square has 4 equal sides: 25 + 25 + 25 + 25 = 100 cm. 75 cm forgets one side.", 1000)
    add("The class bulletin board is 120 cm long and 90 cm wide. Mr. Singh puts a paper border around it. "
        "How long is the border?", "420 cm", ["210 cm", "330 cm", "300 cm"],
        "Add all 4 sides: 120 + 90 + 120 + 90 = 420 cm. 210 cm is only one length and one width.", 4200)
    add("A park is shaped like a triangle. Its sides are 120 m, 150 m and 90 m. Arjun walks once around the park. "
        "How far does he walk?", "360 m", ["270 m", "260 m", "370 m"],
        "Add the 3 sides: 120 + 150 + 90 = 360 m.", 360000)
    add("Liam’s family makes a backyard skating rink that is 10 m long and 6 m wide. They put boards around all "
        "the edges. How many metres of boards do they need?", "32 m", ["16 m", "60 m", "26 m"],
        "Boards go around all 4 sides: 10 + 6 + 10 + 6 = 32 m. 60 would be the area of the rink.", 32000)
    add("A dog pen is 9 m long and 4 m wide. One long side is the wall of the house, so it needs no fence. "
        "How much fence is needed for the other 3 sides?", "17 m", ["26 m", "22 m", "13 m"],
        "Only 3 sides get fence: 4 + 9 + 4 = 17 m. 26 m would put fence along the house wall too.", 17000)
    add("Kai’s family paddles their canoe 3 km to an island and 3 km back to the cottage. How far do they paddle?",
        "6 km", ["6 m", "3 km", "9 km"], "There and back is 3 km + 3 km = 6 km.", 6000000)
    add("The CN Tower in Toronto is 553 m tall. How much less than 1 km is that?", "447 m",
        ["457 m", "547 m", "1553 m"],
        "1 km = 1000 m. 1000 − 553 = 447 m. Check: 553 + 447 = 1000.", 447000)
    add("A ladybug is 7 mm long. A beetle is 3 cm long. How much longer is the beetle?", "23 mm",
        ["4 mm", "4 cm", "37 mm"],
        "Change to the same unit first: 3 cm = 30 mm. 30 − 7 = 23 mm. Do not take 3 from 7.", 23)
    add("Ethan used 30 m of fence to go around a rectangular garden. The garden is 9 m long. How wide is it?",
        "6 m", ["21 m", "12 m", "15 m"],
        "Two lengths: 9 + 9 = 18 m. 30 − 18 = 12 m for the two widths. 12 ÷ 2 = 6 m.", 6000)
    add("A square sandbox has a perimeter of 12 m. How long is each side?", "3 m", ["6 m", "4 m", "8 m"],
        "A square has 4 equal sides. 12 ÷ 4 = 3 m. Check: 3 + 3 + 3 + 3 = 12.", 3000)
    add("Garden A is 8 m by 2 m. Garden B is 5 m by 5 m. Which garden needs more fence to go around it?",
        "They need the same, 20 m", ["B, because it is bigger", "A, because it is longer", "B, it needs 25 m"],
        "A: 8 + 2 + 8 + 2 = 20 m. B: 5 + 5 + 5 + 5 = 20 m. They need the same fence. B has more space inside "
        "(25 is its area), but the same perimeter.")
    add("A rug is 3 m long and 2 m wide. Ava sews a strip of trim around all the edges. How much trim does "
        "she use?", "10 m", ["6 m", "5 m", "8 m"],
        "Perimeter = 3 + 2 + 3 + 2 = 10 m. 6 is the area of the rug, and 5 m is only two sides.", 10000)
    add("Maya wants to put tape around the edge of a table that is 90 cm long and 60 cm wide. She has 250 cm of "
        "tape. Is that enough?", "No, the edge is 300 cm",
        ["Yes, the edge is 150 cm", "Yes, the edge is 240 cm", "No, the edge is 5400 cm"],
        "Perimeter = 90 + 60 + 90 + 60 = 300 cm. 300 cm is more than 250 cm, so it is not enough. "
        "150 cm is only one length and one width.")
    add("Mei cuts out a sign shaped like a hexagon. All 6 sides are 15 cm long. She puts gold ribbon around the "
        "edge. How much ribbon does she use?", "90 cm", ["75 cm", "21 cm", "105 cm"],
        "6 sides of 15 cm: 15 + 15 + 15 + 15 + 15 + 15 = 90 cm. 75 cm leaves out one side.", 900)
    add("A soccer field at the park is 100 m long and 60 m wide. Owen jogs once around it. How far does he jog?",
        "320 m", ["160 m", "260 m", "220 m"],
        "Add all 4 sides: 100 + 60 + 100 + 60 = 320 m. 160 m is only half of the way around.", 320000)
    add("Noah has 85 cm of ribbon. He cuts off 30 cm to wrap a gift. How much ribbon is left?",
        "55 cm", ["115 cm", "65 cm", "55 m"], "Cutting off means subtract: 85 − 30 = 55 cm.", 550)
    assert len(its) == 20, len(its)
    return {"title": "Word problems: fences, rinks and runs", "items": its}


# ------------------------------------------------------------ lesson
def ex(title, q, s, a):
    return ("<div class='sn-ex'><span class='sn-ex-t'>%s</span><p class='sn-ex-q'>%s</p>"
            "<p class='sn-ex-s'>%s</p><p class='sn-ex-a'>Answer: %s</p></div>" % (title, q, s, a))


def table(head, rows, cls="sn-table"):
    h = "".join("<th>%s</th>" % x for x in head)
    b = "".join("<tr>" + "".join("<td>%s</td>" % x for x in r) + "</tr>" for r in rows)
    return "<div class='sn-tw'><table class='%s'><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>" % (cls, h, b)


LESSON_Q = [8, 7, 10, 6]                       # in proportion to QUAD[0]


def body_html():
    return (
        "<h2>Units of length</h2>"
        "<p>Length is how long something is. Small things use small units. Long distances use big units.</p>" +
        table(["Unit", "Benchmark (about this long)", "Use it for"], [
            ["millimetre (mm)", "the thickness of a dime", "a ladybug, a loonie’s thickness"],
            ["centimetre (cm)", "the width of your fingernail", "a pencil, a notebook"],
            ["metre (m)", "a metre stick, or one big step", "a door, a hockey rink"],
            ["kilometre (km)", "a 15-minute walk", "the Terry Fox Run, a trip to Ottawa"],
        ]) +
        "<p>Key facts: 1 cm = 10 mm, 1 m = 100 cm, 1 km = 1000 m.</p>"
        "<h2>Measure with a ruler</h2>"
        "<p>Line up one end of the object with <b>0</b>, not with 1 and not with the edge of the ruler. "
        "Read the number at the other end.</p>"
        "<figure class='sn-fig'>" + ruler_svg(0, 70, "pencil") +
        "<figcaption>The pencil starts at 0 and ends at 7. It is 7 cm long.</figcaption></figure>"
        "<p>If the object does not start at 0, take away the start from the end, or count the spaces.</p>"
        "<figure class='sn-fig'>" + ruler_svg(20, 90, "crayon") +
        "<figcaption>The crayon starts at 2 and ends at 9. 9 − 2 = 7, so it is 7 cm long, not 9 cm.</figcaption></figure>"
        "<h2>Perimeter: the distance around</h2>"
        "<p>Perimeter is the <b>distance all the way around</b> a flat shape. To find it, <b>add every side</b>.</p>"
        "<figure class='sn-fig'>" + grid_svg(5, 3, rect_cells(5, 3), cell=34, label="rectangle 5 by 3 on a grid") +
        "<figcaption>Each square is 1 cm on each side. 5 + 3 + 5 + 3 = 16 cm. "
        "(The 15 squares inside are the area.)</figcaption></figure>"
        "<figure class='sn-fig'>" + polygon_svg(QUAD[0], ["%d cm" % v for v in LESSON_Q],
                                                "quadrilateral with side lengths") +
        "<figcaption>%s = %d cm.</figcaption></figure>" % (plus(LESSON_Q), sum(LESSON_Q)) +
        "<p>For a curved side, lay a string along the edge, then measure the string with a ruler.</p>" +
        ex("Fence a garden", "A garden is 8 m long and 3 m wide. How much fence goes around it?",
           "A rectangle has 4 sides, even when only 2 numbers are given: 8 + 3 + 8 + 3 = 22.", "22 m") +
        ex("Find a missing side", "A triangle has a perimeter of 20 cm. Two sides are 6 cm and 8 cm.",
           "Add the sides you know: 6 + 8 = 14. Subtract: 20 − 14 = 6.", "6 cm") +
        "<h2>Common mistakes</h2>" +
        table(["Mistake", "What to do instead"], [
            ["Starting at 1 or at the edge of the ruler", "Start at 0, or take away the start from the end"],
            ["Counting the marks (0 to 6 is 7 marks)", "Count the spaces: 0 to 6 is 6 cm"],
            ["Choosing km for a pencil", "Pick a unit that fits the size: mm, cm, m or km"],
            ["Adding only the two numbers shown on a rectangle", "Add all 4 sides: 8 + 3 + 8 + 3"],
            ["Counting the squares inside", "That is the area. Perimeter counts the edges around"],
        ])
    )


FAQ = [
    {"q": "What do Grade 3 students learn about length and perimeter in Ontario?",
     "a": "In the Spatial Sense strand, Grade 3 students choose mm, cm, m or km, estimate with benchmarks, "
          "measure even when an object does not start at 0, and find the perimeter of polygons and curved shapes."},
    {"q": "What is the difference between perimeter and area?",
     "a": "Perimeter is the distance around the edge of a shape, in cm or m. Area is the space inside, "
          "counted in squares. A 5 cm by 3 cm rectangle has a perimeter of 16 cm and an area of 15 square centimetres."},
    {"q": "How do you measure when the object does not start at 0 on the ruler?",
     "a": "Subtract the start number from the end number, or count the spaces between them. "
          "A pencil from 2 cm to 9 cm is 9 − 2 = 7 cm long."},
    {"q": "Is perimeter on the Grade 3 EQAO math assessment?",
     "a": "The Grade 3 EQAO math assessment is based on the Ontario curriculum, which includes length and "
          "perimeter, so students may see questions like these. These worksheets are good practice."},
]


def balance(sets, rnd):
    """Spread the correct answers evenly over the 4 positions in every set."""
    for s in sets:
        targets = [0, 1, 2, 3] * 5
        rnd.shuffle(targets)
        for it, t in zip(s["items"], targets):
            ch = it["c"]
            ch[it["a"]], ch[t] = ch[t], ch[it["a"]]
            it["a"] = t


def gen_unit():
    rnd = random.Random(33811)
    sets = [set_units(rnd), set_ruler(rnd), set_add(rnd), set_missing(rnd), set_story(rnd)]
    balance(sets, rnd)
    seen = set()
    for s in sets:
        assert len(s["items"]) == 20, (s["title"], len(s["items"]))
        pos = [0, 0, 0, 0]
        for it in s["items"]:
            assert len(set(it["c"])) == 4, it
            vals = [parse(x) for x in it["c"]]
            vals = [v for v in vals if v is not None]
            assert len(vals) == len(set(vals)), it
            pos[it["a"]] += 1
            k = re.sub(r"<[^>]+>", "", it["q"]) + "|" + it["q"][:300] + "|".join(sorted(it["c"]))
            assert k not in seen, it["q"]
            seen.add(k)
            assert it["q"].count("<svg") <= 1
        assert pos == [5, 5, 5, 5], (s["title"], pos)
    return {
        "country": "ca-on", "subject": "math", "grade": "grade-3", "slug": "length-and-perimeter", "sort": 11,
        "updated": UPDATED, "pdf_url": "",
        "title": "Length and Perimeter",
        "seo_title": "Grade 3 Length and Perimeter Worksheets (Free, with Answer Key) | Ontario Math",
        "short_title": "Length and perimeter",
        "domain": "Spatial Sense",
        "standard_code": "Grade 3: E2.1",
        "standard_url": "https://www.dcp.edu.gov.on.ca/en/curriculum/elementary-mathematics",
        "standard_text": "Use appropriate units of length to estimate, measure, and compare the perimeters of "
                         "polygons and curved shapes, and construct polygons with a given perimeter",
        "meta_desc": "Free Grade 3 math worksheets on length and perimeter: choose mm, cm, m or km, use benchmarks, "
                     "measure with a ruler even when it does not start at 0, add sides, find a missing side and "
                     "solve fence and hockey rink word problems. 100 questions with an answer key, matched to the "
                     "Ontario curriculum and good EQAO practice.",
        "key_big": "Start at 0, count the spaces, and add every side to find the perimeter.",
        "key_sub": "1 cm = 10 mm, 1 m = 100 cm and 1 km = 1000 m. A rectangle has 4 sides even when only "
                   "2 numbers are shown: 8 + 3 + 8 + 3 = 22.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }


def mark_large(u, pattern):
    """Tag pictures that must print larger so their labels stay readable."""
    rx = re.compile(r"<svg (?=[^>]*aria-label='" + pattern + ")")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u


if __name__ == "__main__":
    u = gen_unit()
    mark_large(u, "ruler")
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
