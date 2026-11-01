# -*- coding: utf-8 -*-
"""
US Grade 4 Math: Area and Perimeter Formulas (4.MD.A.3)
  python tools/gen_us_math_g4_area_perimeter.py
HTML attributes use single quotes (no backslashes in the JSON).
Grade 4 style: numbers 1,000 and above are written with commas.
"""
import json, math, os, random, re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "us", "math", "grade-4")
UPDATED = "2026-11-02"
GREEN = "#006633"
FILL = "#cfe6d6"
RED = "#c0392b"
INK = "#2b2b2b"
FONT = "Arial, Helvetica, sans-serif"
GIRLS = ["Maya", "Ava", "Mia", "Zoe", "Lily", "Emma", "Nora", "Ruby", "Sofia", "Grace"]
BOYS = ["Leo", "Noah", "Eli", "Sam", "Ben", "Omar", "Kai", "Jack", "Luis", "Owen"]
UNITS = [("cm", "sq cm"), ("m", "sq m"), ("in", "sq in"), ("ft", "sq ft")]


# ------------------------------------------------------------ helpers
def f(n):
    """Grade 4 style: 4536 -> 4,536."""
    return "{:,}".format(n)


def mcq(q, correct, cands, e, rnd):
    """4 choices: correct + 3 unique distractors (no zero or negative numbers)."""
    correct = str(correct)
    seen = {correct}
    pick = []
    for c in cands:
        c = str(c)
        lead = c.split(" ")[0].lstrip("$")
        if c in seen or not c or lead.startswith("-") or lead == "0":
            continue
        seen.add(c)
        pick.append(c)
        if len(pick) == 3:
            break
    assert len(pick) == 3, (q, correct, cands)
    ch = pick + [correct]
    rnd.shuffle(ch)
    return {"q": q, "c": ch, "a": ch.index(correct), "e": e}


class People:
    def __init__(self, rnd):
        self.pool = [(n, "she", "her") for n in GIRLS] + [(n, "he", "his") for n in BOYS]
        rnd.shuffle(self.pool)
        self.i = 0

    def next(self):
        p = self.pool[self.i % len(self.pool)]
        self.i += 1
        return p


def an(n):
    """'an 11', 'an 8', 'a 12'."""
    return "an" if str(n)[0] == "8" or n in (11, 18) else "a"


def cap(s):
    return s[0].upper() + s[1:]


def fig(svg):
    return "<div class='qfig'>" + svg + "</div>"


def svg_wrap(w, h, body, label):
    return ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 %d %d' width='%d' height='%d' "
            "role='img' aria-label='%s'><g font-family='%s'>%s</g></svg>" % (w, h, w, h, label, FONT, body))


def tw(t, fs):
    """Approximate width of bold Arial text in px. Commas and spaces are narrow."""
    t = str(t)
    return (len(t) - t.count(",") * 0.6 - t.count(" ") * 0.3) * fs * 0.6


def text(x, y, t, fs=17, col=INK):
    return ("<text x='%.1f' y='%.1f' font-size='%d' font-weight='700' fill='%s' text-anchor='middle'>%s</text>"
            % (x, y, fs, col, t))


# ------------------------------------------------------------ figures
FS = 17          # side labels
FS_IN = 16       # text inside a shape


def shape_svg(pts, labels, label, inside=None, dashed=None):
    """Polygon with straight (horizontal or vertical) sides, drawn to scale.
    pts are pixel points; labels[i] belongs to the side from pts[i] to pts[i+1] ('' = no label,
    a label with '?' is red). Each label sits just outside the middle of its side.
    inside = lines of text written in the middle of the shape; dashed = (x1, y1, x2, y2) split line.
    A label that would overlap another label or a side slides along its side.
    Returns None if no place is found."""
    n = len(pts)
    sa = sum(pts[i][0] * pts[(i + 1) % n][1] - pts[(i + 1) % n][0] * pts[i][1] for i in range(n))
    def clash(bx, placed):
        for B in placed:                     # keep a clear gap so each label belongs to one side
            if bx[0] < B[2] + 16 and B[0] < bx[2] + 16 and bx[1] < B[3] + 8 and B[1] < bx[3] + 8:
                return True
        for i in range(n):
            (x1, y1), (x2, y2) = pts[i], pts[(i + 1) % n]
            if x1 == x2:
                if bx[0] - 3 < x1 < bx[2] + 3 and min(y1, y2) < bx[3] and bx[1] < max(y1, y2):
                    return True
            elif bx[1] - 3 < y1 < bx[3] + 3 and min(x1, x2) < bx[2] and bx[0] < max(x1, x2):
                return True
        return False

    boxes, texts = [], []
    if inside:
        for j, t in enumerate(inside[2]):
            yy = inside[1] + (j - (len(inside[2]) - 1) / 2) * 21
            hw = tw(t, FS_IN) / 2
            bx = (inside[0] - hw, yy - 8, inside[0] + hw, yy + 8)
            if clash(bx, []):
                return None
            boxes.append(bx)
    boxes_in = len(boxes)
    for i in range(n):
        t = labels[i]
        if not t:
            continue
        (x1, y1), (x2, y2) = pts[i], pts[(i + 1) % n]
        dx, dy = x2 - x1, y2 - y1
        L = math.hypot(dx, dy) or 1
        nx, ny = (dy / L, -dx / L) if sa > 0 else (-dy / L, dx / L)       # outward normal
        hw = tw(t, FS) / 2
        off = 8 + abs(nx) * hw + abs(ny) * 11
        for fr in (0.5, 0.62, 0.38, 0.72, 0.28, 0.8, 0.2):                  # slide along the side if needed
            mx, my = x1 + dx * fr, y1 + dy * fr
            cx, cy = mx + nx * off, my + ny * off
            bx = (cx - hw, cy - 11, cx + hw, cy + 11)
            if not clash(bx, boxes):
                break
        else:
            return None
        boxes.append(bx)
        texts.append((cx, cy, t))
    xs = [p[0] for p in pts] + [b[0] for b in boxes] + [b[2] for b in boxes]
    ys = [p[1] for p in pts] + [b[1] for b in boxes] + [b[3] for b in boxes]
    pad = 5
    ox, oy = min(xs) - pad, min(ys) - pad
    W, H = int(math.ceil(max(xs) - ox + pad)), int(math.ceil(max(ys) - oy + pad))
    s = ["<polygon points='%s' fill='%s' stroke='%s' stroke-width='3' stroke-linejoin='round'/>"
         % (" ".join("%.0f,%.0f" % (x - ox, y - oy) for x, y in pts), FILL, GREEN)]
    if dashed:
        x1, y1, x2, y2 = dashed
        s.append("<line x1='%.0f' y1='%.0f' x2='%.0f' y2='%.0f' stroke='%s' stroke-width='2.5' stroke-dasharray='7 5'/>"
                 % (x1 - ox, y1 - oy, x2 - ox, y2 - oy, RED))
    for cx, cy, t in texts:
        s.append(text(cx - ox, cy - oy + 6, t, FS, RED if "?" in t else INK))
    if inside:
        for j, t in enumerate(inside[2]):
            yy = inside[1] + (j - (len(inside[2]) - 1) / 2) * 21
            s.append(text(inside[0] - ox, yy - oy + 6, t, FS_IN, GREEN))
    return svg_wrap(W, H, "".join(s), label)


def rect_pts(L, W, max_w=200, max_h=105):
    k = min(max_w / L, max_h / W, 26)
    return [(0, 0), (L * k, 0), (L * k, W * k), (0, W * k)]


def rect_svg(L, W, top, left, label, inside=None):
    """Rectangle drawn to scale: length L across, width W down. Labels on the top and left sides."""
    pts = rect_pts(L, W, max_h=105 if not inside else 100)
    ins = None
    if inside:
        ins = (pts[2][0] / 2, pts[2][1] / 2, inside)
    s = shape_svg(pts, [top, "", "", left], label, ins)
    assert s, (L, W, top, left, inside)
    return s


def l_pts(Wt, Ht, cw, ch, corner, k):
    """L shape: a Wt by Ht rectangle with a cw by ch piece cut from one corner.
    Sides in order: [Wt - cw, ch, cw, Ht - ch, Wt, Ht] (same order for every corner)."""
    p = [(0, 0), (Wt - cw, 0), (Wt - cw, ch), (Wt, ch), (Wt, Ht), (0, Ht)]
    if corner in ("tl", "bl"):
        p = [(Wt - x, y) for x, y in p]
    if corner in ("br", "bl"):
        p = [(x, Ht - y) for x, y in p]
    return [(x * k, y * k) for x, y in p]


def l_svg(Wt, Ht, cw, ch, corner, labels, label, split=False):
    k = min(250 / Wt, 140 / Ht)
    pts = l_pts(Wt, Ht, cw, ch, corner, k)
    dashed = None
    if split:                       # vertical line from the inner corner across the shape
        x = (Wt - cw) * k if corner in ("tr", "br") else cw * k
        dashed = (x, ch * k, x, Ht * k) if corner in ("tr", "tl") else (x, 0, x, (Ht - ch) * k)
    return shape_svg(pts, labels, label, dashed=dashed)


# ------------------------------------------------------------ typical mistakes
def two_pp(a, b):
    """Only tens × tens and ones × ones: 24 × 15 -> 200 + 20."""
    return (a // 10) * (b // 10) * 100 + (a % 10) * (b % 10)


def no_zero(a, b):
    """Forgot the zero when multiplying by the tens: 24 × 5 + 24 × 1."""
    return a * (b % 10) + a * (b // 10)


def mult_steps(a, b):
    """24 × 15: 24 × 10 = 240, 24 × 5 = 120, 240 + 120 = 360."""
    if b < 10 or b % 10 == 0:
        return ""
    t, o = b - b % 10, b % 10
    return " (%d × %d = %s, %d × %d = %s, %s + %s = %s)" % (a, t, f(a * t), a, o, f(a * o), f(a * t), f(a * o), f(a * b))


def area_e(L, W, su):
    return "Area = length × width = %d × %d = %s %s%s." % (L, W, f(L * W), su, mult_steps(L, W))


def per_e(L, W, u):
    return ("Perimeter = 2 × length + 2 × width = 2 × %d + 2 × %d = %s + %s = %s %s."
            % (L, W, f(2 * L), f(2 * W), f(2 * (L + W)), u))


# ------------------------------------------------------------ set 1: use the formulas
def pick_rect(rnd, seen, lr, wr, ratio=3.2):
    while True:
        L, W = rnd.randint(*lr), rnd.randint(*wr)
        if L <= W or L / W > ratio or (L, W) in seen or L * W == 2 * (L + W):
            continue
        seen.add((L, W))
        return L, W


def set_formulas(rnd, seen):
    its = []
    for i in range(16):
        L, W = pick_rect(rnd, seen, (4, 12), (2, 9))
        u, su = UNITS[i % 4]
        A, P = L * W, 2 * (L + W)
        pic = i % 4 in (0, 1)
        if i % 2 == 0:                                   # area
            q = (fig(rect_svg(L, W, "%d %s" % (L, u), "%d %s" % (W, u), "rectangle %d by %d" % (L, W))) +
                 "What is the area of the rectangle?") if pic else \
                "A rectangle is %d %s long and %d %s wide. What is its area?" % (L, u, W, u)
            cands = ([P, A, L + W], [su, u, su]) if i % 4 == 0 else ([A, P, L + W], [u, su, su])
            cands = ["%s %s" % (f(v), un) for v, un in zip(*cands)]
            e = area_e(L, W, su) + " Area counts squares, so the unit is %s. (%d is the perimeter.)" % (su, P)
            its.append(mcq(q, "%d %s" % (A, su), cands, e, rnd))
        else:                                            # perimeter
            q = (fig(rect_svg(L, W, "%d %s" % (L, u), "%d %s" % (W, u), "rectangle %d by %d" % (L, W))) +
                 "What is the perimeter of the rectangle?") if pic else \
                "A rectangle is %d %s long and %d %s wide. What is its perimeter?" % (L, u, W, u)
            cands = ["%d %s" % (A, u), "%d %s" % (L + W, u), "%d %s" % (P, su), "%d %s" % (2 * L + W, u)]
            if i % 4 == 3:
                cands = [cands[3], cands[1], cands[0]]
            e = per_e(L, W, u) + " Adding only %d + %d = %d leaves out two sides." % (L, W, L + W)
            its.append(mcq(q, "%d %s" % (P, u), cands, e, rnd))
    for k, s in enumerate(rnd.sample(range(3, 11), 4)):  # squares
        u, su = UNITS[(k + 1) % 4]
        A, P = s * s, 4 * s
        if k % 2 == 0:
            q = (fig(rect_svg(s, s, "%d %s" % (s, u), "", "square with %d %s sides" % (s, u))) +
                 "This is a square. What is its area?")
            its.append(mcq(q, "%d %s" % (A, su), ["%d %s" % (P, su), "%d %s" % (2 * s, su), "%d %s" % (A, u)],
                           "All 4 sides of a square are %d %s. Area = %d × %d = %d %s." % (s, u, s, s, A, su), rnd))
        else:
            q = "A square has sides that are %d %s long. What is its perimeter?" % (s, u)
            its.append(mcq(q, "%d %s" % (P, u), ["%d %s" % (A, u), "%d %s" % (2 * s, u), "%d %s" % (P, su)],
                           "A square has 4 equal sides: 4 × %d = %d %s. (%d × %d = %d would be the area.)"
                           % (s, P, u, s, s, A), rnd))
    rnd.shuffle(its)
    return {"title": "Use the area and perimeter formulas", "items": its}


# ------------------------------------------------------------ set 2: bigger numbers, which formula fits
def pick_big(rnd, seen):
    while True:
        L, W = rnd.randint(13, 48), rnd.randint(11, 29)
        if L <= W or L / W > 3 or L % 10 == 0 or W % 10 == 0 or (L, W) in seen:
            continue
        if two_pp(L, W) == no_zero(L, W) or (L % 10) * (W % 10) < 10:
            continue
        seen.add((L, W))
        return L, W


EQ_CTX = [  # (question with {L} {W} {u}, area?)
    ("A farmer puts a fence around a field that is {L} {uw} long and {W} {uw} wide. Which equation finds the length of the fence?", False),
    ("A family buys carpet for a floor that is {L} {uw} long and {W} {uw} wide. Which equation finds how much carpet covers the floor?", True),
    ("A class glues a paper border around a bulletin board that is {L} {uw} long and {W} {uw} tall. Which equation finds the length of the border?", False),
    ("A park plants grass on a lawn that is {L} {uw} long and {W} {uw} wide. Which equation finds the area of grass?", True),
    ("A runner jogs once around a parking lot that is {L} {uw} long and {W} {uw} wide. Which equation finds how far the runner goes?", False),
    ("A painter covers a wall that is {L} {uw} wide and {W} {uw} tall. Which equation finds how much wall gets painted?", True),
    ("A tailor sews lace along every edge of a pillow cover that is {L} {uw} long and {W} {uw} wide. Which equation finds the length of the lace?", False),
    ("A school puts mats on a gym floor that is {L} {uw} long and {W} {uw} wide. Which equation finds how much floor the mats cover?", True),
]
EQ_UNITS = {0: ("m", "meters"), 1: ("ft", "feet"), 2: ("in", "inches"), 3: ("m", "meters"), 4: ("m", "meters"),
            5: ("ft", "feet"), 6: ("in", "inches"), 7: ("ft", "feet")}


def set_big(rnd, seen):
    its = []
    for i in range(12):
        L, W = pick_big(rnd, seen)
        u, su = UNITS[i % 4]
        A, P = L * W, 2 * (L + W)
        pic = i % 3 != 2
        if i % 2 == 0:
            q = (fig(rect_svg(L, W, "%d %s" % (L, u), "%d %s" % (W, u), "rectangle %d by %d" % (L, W))) +
                 "What is the area of the rectangle?") if pic else \
                "A rectangle is %d %s long and %d %s wide. What is its area?" % (L, u, W, u)
            pool = [("%s %s" % (f(no_zero(L, W)), su)), ("%s %s" % (f(two_pp(L, W)), su)),
                    ("%s %s" % (f(P), su)), ("%s %s" % (f(A), u))]
            r = (i // 2) % 4
            pool = pool[r:] + pool[:r]
            e = (area_e(L, W, su) + " Multiply every part: %d × %d is not only %d × %d plus %d × %d."
                 % (L, W, L - L % 10, W - W % 10, L % 10, W % 10))
            its.append(mcq(q, "%s %s" % (f(A), su), pool, e, rnd))
        else:
            q = (fig(rect_svg(L, W, "%d %s" % (L, u), "%d %s" % (W, u), "rectangle %d by %d" % (L, W))) +
                 "What is the perimeter of the rectangle?") if pic else \
                "A rectangle is %d %s long and %d %s wide. What is its perimeter?" % (L, u, W, u)
            pool = ["%d %s" % (L + W, u), "%d %s" % (2 * L + W, u), "%s %s" % (f(A), u), "%d %s" % (P, su)]
            r = (i // 2) % 4
            pool = pool[r:] + pool[:r]
            e = per_e(L, W, u) + " Or add first: %d + %d = %d, then 2 × %d = %d %s." % (L, W, L + W, L + W, P, u)
            its.append(mcq(q, "%d %s" % (P, u), pool, e, rnd))
    for k, (t, is_area) in enumerate(EQ_CTX):
        L, W = pick_big(rnd, seen)
        u, uw = EQ_UNITS[k]
        q = t.format(L=L, W=W, uw=uw)
        ar = "A = %d × %d" % (L, W)
        pe = "P = 2 × %d + 2 × %d" % (L, W)
        if is_area:
            right, wrong = ar, [pe, "A = %d + %d" % (L, W), "A = %d × %d × 2" % (L, W)]
            e = ("Covering a surface is area, so multiply length × width: %s = %s sq %s. "
                 "The perimeter equation finds the distance around." % (ar, f(L * W), u))
        else:
            right, wrong = pe, [ar, "P = %d + %d" % (L, W), "P = 2 × %d + %d" % (L, W)]
            e = ("Going around the edge is perimeter: 2 lengths + 2 widths = %s + %s = %d %s. "
                 "%d × %d finds the area inside." % (f(2 * L), f(2 * W), 2 * (L + W), u, L, W))
        its.append(mcq(q, right, wrong, e, rnd))
    rnd.shuffle(its)
    return {"title": "Bigger numbers and the right formula", "items": its}


# ------------------------------------------------------------ set 3: unknown side
def set_unknown(rnd, seen):
    its = []
    # area and length -> width (picture)
    for i in range(6):
        L, W = pick_rect(rnd, seen, (6, 12), (3, 9), ratio=2.6)
        u, su = UNITS[i % 4]
        A = L * W
        if i % 2 == 0:
            top, left, ans, known = "%d %s" % (L, u), "? %s" % u, W, L
        else:
            top, left, ans, known = "? %s" % u, "%d %s" % (W, u), L, W
        q = (fig(rect_svg(L, W, top, left, "rectangle with area %d and one unknown side" % A,
                          inside=["Area =", "%d %s" % (A, su)])) +
             "The area of the rectangle is %d %s. What is the length of the side marked ?" % (A, su))
        cands = ["%d %s" % (A - known, u), "%d %s" % (ans, su), "%d %s" % (A // 2 - known, u) if A % 2 == 0 else "",
                 "%d %s" % (A + known, u)]
        e = ("Area = length × width, so %d × ? = %d. %d ÷ %d = %d, so the side is %d %s. Check: %d × %d = %d."
             % (known, A, A, known, ans, ans, u, known, ans, A))
        its.append(mcq(q, "%d %s" % (ans, u), cands, e, rnd))
    # area and one side -> other side (no picture, bigger)
    for i, (A, s, u, su) in enumerate([(96, 8, "cm", "sq cm"), (126, 7, "ft", "sq ft"), (156, 6, "m", "sq m"),
                                       (108, 9, "in", "sq in")]):
        o = A // s
        w1, w2 = ("width", "length") if i % 2 == 0 else ("length", "width")
        q = "A rectangle has an area of %d %s. Its %s is %d %s. What is its %s?" % (A, su, w1, s, u, w2)
        cands = ["%d %s" % (A - s, u), "%d %s" % (A // 2 - s, u), "%d %s" % (o, su), "%d %s" % (A + s, u)]
        e = ("Think of the area formula with a missing factor: %d × ? = %d. Divide: %d ÷ %d = %d %s. Check: %d × %d = %d."
             % (s, A, A, s, o, u, s, o, A))
        its.append(mcq(q, "%d %s" % (o, u), cands, e, rnd))
    # perimeter and length -> width
    for i in range(6):
        L, W = pick_rect(rnd, seen, (9, 25), (4, 16), ratio=3)
        u, su = UNITS[(i + 2) % 4]
        P = 2 * (L + W)
        cands = ["%d %s" % (P - L, u), "%d %s" % (P - 2 * L, u), "%d %s" % (P // 2, u), "%d %s" % (L * 2, u)]
        e = ("The two lengths are 2 × %d = %d. %d − %d = %d for the two widths, so each width is %d ÷ 2 = %d %s. "
             "Check: %d + %d + %d + %d = %d." % (L, 2 * L, P, 2 * L, 2 * W, 2 * W, W, u, L, W, L, W, P))
        if i < 3:
            q = (fig(rect_svg(L, W, "%d %s" % (L, u), "? %s" % u, "rectangle with perimeter %d and unknown width" % P,
                              inside=["Perimeter =", "%d %s" % (P, u)])) +
                 "The perimeter of the rectangle is %d %s. What is the width marked ?" % (P, u))
        else:
            q = "A rectangle has a perimeter of %d %s. It is %d %s long. How wide is it?" % (P, u, L, u)
        its.append(mcq(q, "%d %s" % (W, u), cands, e, rnd))
    # which equation finds the unknown side?
    for k in range(4):
        L, W = pick_rect(rnd, seen, (7, 15), (3, 9), ratio=4)
        u, su = UNITS[k]
        if k % 2 == 0:
            A = L * W
            q = ("A rectangle has an area of %d %s. It is %d %s long. Which equation can you use to find the width, w?"
                 % (A, su, L, u))
            right = "%d × w = %d" % (L, A)
            wrong = ["%d + w = %d" % (L, A), "2 × %d + 2 × w = %d" % (L, A), "w = %d × %d" % (A, L)]
            e = ("Area = length × width, so %d × w = %d. Then w = %d ÷ %d = %d %s."
                 % (L, A, A, L, W, u))
        else:
            P = 2 * (L + W)
            q = ("A rectangle has a perimeter of %d %s. It is %d %s long. Which equation can you use to find the width, w?"
                 % (P, u, L, u))
            right = "2 × %d + 2 × w = %d" % (L, P)
            wrong = ["%d × w = %d" % (L, P), "%d + w = %d" % (L, P), "2 × %d + w = %d" % (L, P)]
            e = ("Perimeter = 2 × length + 2 × width, so 2 × %d + 2 × w = %d. %d + 2 × w = %d, 2 × w = %d, w = %d %s."
                 % (L, P, 2 * L, P, 2 * W, W, u))
        its.append(mcq(q, right, wrong, e, rnd))
    rnd.shuffle(its)
    return {"title": "Find the unknown side", "items": its}


# ------------------------------------------------------------ set 4: area or perimeter? squares
DECIDE = [  # (text with {n} {he} {his}, area?, length unit)
    ("{n} wants to buy carpet to cover {his} bedroom floor. What should {he} find?", True, "ft"),
    ("{n} is building a fence around a vegetable garden. What should {he} find?", False, "m"),
    ("{n} is putting a paper border around the edge of a bulletin board. What should {he} find?", False, "ft"),
    ("{n} needs grass seed to cover a lawn. What should {he} find?", True, "m"),
    ("{n} is buying tiles to cover a bathroom floor. What should {he} find?", True, "ft"),
    ("{n} wants to hang a string of lights around the edge of a window. What should {he} find?", False, "in"),
    ("{n} is covering the top of {his} desk with paper. What should {he} find?", True, "in"),
    ("{n} is running laps around the edge of a soccer field. What should {he} find?", False, "m"),
]


def set_decide(rnd, P):
    its = []
    for t, is_area, u in DECIDE:
        n, he, his = P.next()
        q = t.format(n=n, he=he, his=his)
        ra, rp, wa, wp = "Area, sq %s" % u, "Perimeter, %s" % u, "Area, %s" % u, "Perimeter, sq %s" % u
        if is_area:
            e = ("Covering a surface means the space inside, so find the area. "
                 "Area is measured in square units: sq %s." % u)
            its.append(mcq(q, ra, [rp, wa, wp], e, rnd))
        else:
            e = ("Going along the edge means the distance around, so find the perimeter. "
                 "Perimeter is a length: %s, not square units." % u)
            its.append(mcq(q, rp, [ra, wp, wa], e, rnd))
    # squares
    for k, s in enumerate([13, 16]):
        u, su = UNITS[k * 2 + 1]
        A, Pm = s * s, 4 * s
        q = (fig(rect_svg(s, s, "%d %s" % (s, u), "", "square with %d %s sides" % (s, u))) +
             "This is a square. What is its area?") if k == 0 else \
            "A square patio has sides of %d %s. What is its area?" % (s, u)
        its.append(mcq(q, "%d %s" % (A, su), ["%d %s" % (Pm, su), "%d %s" % (2 * s, su), "%d %s" % (A, u)],
                       "Every side of a square is %d %s, so Area = %d × %d = %d %s%s." % (s, u, s, s, A, su, mult_steps(s, s)), rnd))
    for k, s in enumerate([18, 27]):
        u, su = UNITS[k * 2]
        A, Pm = s * s, 4 * s
        q = (fig(rect_svg(s, s, "%d %s" % (s, u), "", "square with %d %s sides" % (s, u))) +
             "This is a square. What is its perimeter?") if k == 1 else \
            "A square picture has sides of %d %s. What is its perimeter?" % (s, u)
        its.append(mcq(q, "%d %s" % (Pm, u), ["%d %s" % (2 * s, u), "%s %s" % (f(A), u), "%d %s" % (Pm, su)],
                       "A square has 4 equal sides: 4 × %d = %d %s." % (s, Pm, u), rnd))
    for A, u, su in [(64, "ft", "sq ft"), (144, "in", "sq in")]:
        s = int(math.isqrt(A))
        its.append(mcq("A square has an area of %d %s. How long is each side?" % (A, su), "%d %s" % (s, u),
                       ["%d %s" % (A // 4, u), "%d %s" % (A // 2, u), "%d %s" % (s, su)],
                       "Find the number that times itself makes %d: %d × %d = %d. Each side is %d %s. "
                       "(Dividing by 4 works for perimeter, not area.)" % (A, s, s, A, s, u), rnd))
    for Pm, u in [(36, "m"), (100, "cm")]:
        s = Pm // 4
        its.append(mcq("A square has a perimeter of %d %s. How long is each side?" % (Pm, u), "%d %s" % (s, u),
                       ["%d %s" % (int(math.isqrt(Pm)), u), "%d %s" % (Pm // 2, u), "%d %s" % (Pm * 4, u)],
                       "A square has 4 equal sides, so %d ÷ 4 = %d %s. Check: 4 × %d = %d. "
                       "(%d × %d = %d is an area, not a perimeter.)"
                       % (Pm, s, u, s, Pm, math.isqrt(Pm), math.isqrt(Pm), Pm), rnd))
    # compare a rectangle and a square
    ch = ["Same area; A has more perimeter", "Same area; B has more perimeter",
          "Same perimeter; A has more area", "Same perimeter; B has more area"]
    for (a, b, s, u) in [(9, 4, 6, "ft"), (10, 4, 7, "m"), (16, 4, 8, "in"), (11, 5, 8, "cm")]:
        A1, A2, P1, P2 = a * b, s * s, 2 * (a + b), 4 * s
        if A1 == A2:
            right = ch[0] if P1 > P2 else ch[1]
        else:
            assert P1 == P2
            right = ch[2] if A1 > A2 else ch[3]
        q = ("Rectangle A is %d %s by %d %s. Square B has sides of %d %s. Which is true?" % (a, u, b, u, s, u))
        e = ("A: area %d × %d = %d sq %s, perimeter 2 × %d + 2 × %d = %d %s. B: area %d × %d = %d sq %s, "
             "perimeter 4 × %d = %d %s." % (a, b, A1, u, a, b, P1, u, s, s, A2, u, s, P2, u))
        e += (" Same area, but the long, thin rectangle has more edge." if A1 == A2 else
              " Same perimeter, but the square holds more space.")
        its.append(mcq(q, right, [c for c in ch if c != right], e, rnd))
    assert len(its) == 20, len(its)
    rnd.shuffle(its)
    return {"title": "Area or perimeter? Squares", "items": its}


# ------------------------------------------------------------ set 5: L-shapes and word problems
def pick_l(rnd, used):
    while True:
        Wt, Ht = rnd.randint(9, 16), rnd.randint(6, 12)
        if Wt <= Ht or Wt / Ht > 2:
            continue
        cw = rnd.randint(int(math.ceil(Wt * 0.4)), int(Wt * 0.6))
        ch = rnd.randint(int(math.ceil(Ht * 0.4)), int(Ht * 0.6))
        if cw == Wt - cw or ch == Ht - ch or (Wt, Ht, cw, ch) in used:
            continue
        used.add((Wt, Ht, cw, ch))
        return Wt, Ht, cw, ch


L_CTX = [("This is the shape of an L-shaped garden.", "m"), ("This is the floor plan of a room.", "ft"),
         ("This is the shape of a wooden deck.", "ft"), ("This is the shape of a skate park.", "m"),
         ("This is the shape of a patio.", "ft"), ("This is the floor plan of a kitchen.", "ft"),
         ("This is the shape of a swimming area at a lake.", "m"), ("This is a piece of cardboard cut for a model.", "cm")]


def l_item(kind, rnd, used, ctx, u, su):
    corners = ["tr", "tl", "br", "bl"]
    for _ in range(200):
        Wt, Ht, cw, ch = pick_l(rnd, used)
        corner = rnd.choice(corners)
        sides = [Wt - cw, ch, cw, Ht - ch, Wt, Ht]
        labels = ["%d %s" % (v, u) for v in sides]
        A = Wt * Ht - cw * ch
        Pm = 2 * (Wt + Ht)
        A1, A2 = (Wt - cw) * Ht, cw * (Ht - ch)
        if kind == "missing":
            mi = rnd.choice([0, 3])
            labels[mi] = "? %s" % u
        svg = l_svg(Wt, Ht, cw, ch, corner, labels, "L-shaped figure with side lengths", split=(kind == "split"))
        if svg:
            break
    else:
        raise RuntimeError("no L shape fits")
    split_e = ("Split it into two rectangles: %d × %d = %d and %d × %d = %d. Add: %d + %d = %d %s."
               % (Wt - cw, Ht, A1, cw, Ht - ch, A2, A1, A2, A, su))
    cut_e = ("Big rectangle %d × %d = %d, minus the cut-out corner %d × %d = %d: %d − %d = %d %s."
             % (Wt, Ht, Wt * Ht, cw, ch, cw * ch, Wt * Ht, cw * ch, A, su))
    if kind in ("split", "cut"):
        if kind == "split":
            q = fig(svg) + ctx + " The dashed line splits it into two rectangles. What is its area?"
            e = split_e + " Check: " + cut_e[0].lower() + cut_e[1:]
        else:
            q = fig(svg) + ctx + " Think of %s %d by %d rectangle with a corner cut out. What is its area?" % (an(Wt), Wt, Ht)
            e = cut_e + " Check: " + split_e[0].lower() + split_e[1:]
        over = (Wt - cw) * Ht + Wt * (Ht - ch)
        cands = ["%d %s" % (Wt * Ht, su), "%d %s" % (over, su), "%d %s" % (Pm, su), "%d %s" % (A, u)]
        return mcq(q, "%d %s" % (A, su), cands, e, rnd)
    if kind == "per":
        q = fig(svg) + ctx + " What is its perimeter?"
        e = ("Add all 6 sides: %s = %d %s. Do not skip the two short sides at the cut-out corner."
             % (" + ".join(str(v) for v in sides), Pm, u))
        cands = ["%d %s" % (Pm - cw - ch, u), "%d %s" % (A, u), "%d %s" % (Pm, su), "%d %s" % (Pm + cw + ch, u)]
        return mcq(q, "%d %s" % (Pm, u), cands, e, rnd)
    # missing side
    if mi == 0:
        ans, big, small = Wt - cw, Wt, cw
        e = ("The two shorter sides going across, ? and %d %s, together match the long %d %s side. %d − %d = %d %s."
             % (cw, u, Wt, u, Wt, cw, ans, u))
    else:
        ans, big, small = Ht - ch, Ht, ch
        e = ("The two shorter sides going up and down, ? and %d %s, together match the long %d %s side. %d − %d = %d %s."
             % (ch, u, Ht, u, Ht, ch, ans, u))
    q = fig(svg) + ctx + " What is the length of the side marked ?"
    cands = ["%d %s" % (big + small, u), "%d %s" % (big, u), "%d %s" % (ans, su), "%d %s" % (small, u)]
    return mcq(q, "%d %s" % (ans, u), cands, e, rnd)


def set_story(rnd, P):
    its = []
    used = set()
    plan = ["split", "split", "split", "cut", "cut", "per", "per", "missing"]
    ctx = L_CTX[:]
    rnd.shuffle(ctx)
    for i, kind in enumerate(plan):
        c, u = ctx[i]
        its.append(l_item(kind, rnd, used, c, u, "sq " + u))

    # word problems
    n, he, his = P.next()
    A, L = 132, 12
    its.append(mcq("A rectangular bedroom has %d square feet of flooring. The room is %d feet long. How wide is the room?"
                   % (A, L), "%d ft" % (A // L), ["%d ft" % (A - L), "%d ft" % (A // 2 - L), "%d sq ft" % (A // L)],
                   "Area = length × width, so %d × ? = %d. %d ÷ %d = %d. The room is %d feet wide." % (L, A, A, L, A // L, A // L), rnd))
    L, W = 18, 11
    its.append(mcq("%s builds a fence around a rectangular garden that is %d meters long and %d meters wide. "
                   "How many meters of fence does %s need?" % (n, L, W, he), "%d m" % (2 * (L + W)),
                   ["%d m" % (L * W), "%d m" % (L + W), "%d m" % (2 * L + W)],
                   per_e(L, W, "m") + " The fence goes along all 4 sides.", rnd))
    n, he, his = P.next()
    L, W = 36, 24
    its.append(mcq("%s puts ribbon around the edge of a poster that is %d inches tall and %d inches wide. "
                   "How much ribbon does %s need?" % (n, L, W, he), "%d in" % (2 * (L + W)),
                   ["%d in" % (L * W), "%d in" % (L + W), "%d sq in" % (L * W)],
                   "Ribbon goes around the edge, so find the perimeter: 2 × %d + 2 × %d = %d + %d = %d inches. "
                   "(%d sq in is the area of the poster.)" % (L, W, 2 * L, 2 * W, 2 * (L + W), L * W), rnd))
    L, W = 100, 64
    its.append(mcq("A soccer field is %d meters long and %d meters wide. What is the area of the field?" % (L, W),
                   "%s sq m" % f(L * W), ["%d sq m" % (2 * (L + W)), "%s m" % f(L * W), "%d sq m" % (L * W // 10)],
                   "Area = %d × %d = %s sq m. Multiplying by 100 puts two zeros after 64." % (L, W, f(L * W)), rnd))
    n, he, his = P.next()
    L, W, price = 9, 8, 3
    its.append(mcq("%s covers a laundry room floor that is %d feet by %d feet with square tiles. Each tile is 1 square foot "
                   "and costs $%d. How much do the tiles cost?" % (n, L, W, price), "$%d" % (L * W * price),
                   ["$%d" % (2 * (L + W) * price), "$%d" % (L * W), "$%d" % ((L + W) * price)],
                   "Step 1: area = %d × %d = %d sq ft, so %d tiles. Step 2: cost = %d × $%d = $%d."
                   % (L, W, L * W, L * W, L * W, price, L * W * price), rnd))
    L, W = 90, 60
    its.append(mcq("A coach runs around a rectangular field 2 times. The field is %d meters long and %d meters wide. "
                   "How far does the coach run?" % (L, W), "%d m" % (4 * (L + W)),
                   ["%d m" % (2 * (L + W)), "%s m" % f(L * W), "%d m" % (2 * (2 * L + W))],
                   "Once around: 2 × %d + 2 × %d = %d m. Two times around: 2 × %d = %d m."
                   % (L, W, 2 * (L + W), 2 * (L + W), 4 * (L + W)), rnd))
    n, he, his = P.next()
    L, W, a, b = 30, 20, 10, 8
    its.append(mcq("%s's backyard is %d feet long and %d feet wide. A patio that is %d feet by %d feet is in the yard. "
                   "The rest is grass. What is the area of the grass?" % (n, L, W, a, b), "%d sq ft" % (L * W - a * b),
                   ["%d sq ft" % (L * W), "%d sq ft" % (L * W + a * b), "%d sq ft" % ((L - a) * (W - b))],
                   "Whole yard: %d × %d = %d sq ft. Patio: %d × %d = %d sq ft. Grass: %d − %d = %d sq ft."
                   % (L, W, L * W, a, b, a * b, L * W, a * b, L * W - a * b), rnd))
    A, L = 240, 20
    W = A // L
    its.append(mcq("A rectangular dog park has an area of %d square meters. It is %d meters long. "
                   "How many meters of fence go around the park?" % (A, L), "%d m" % (2 * (L + W)),
                   ["%d m" % (L + W), "%d m" % (2 * L + W), "%d m" % W],
                   "Step 1: width = %d ÷ %d = %d m. Step 2: perimeter = 2 × %d + 2 × %d = %d + %d = %d m. "
                   "(%d m is only the width, not the fence.)"
                   % (A, L, W, L, W, 2 * L, 2 * W, 2 * (L + W), W), rnd))
    n, he, his = P.next()
    Pm, L = 86, 25
    its.append(mcq("%s used %d feet of fence to go around a rectangular garden. The garden is %d feet long. "
                   "How wide is it?" % (n, Pm, L), "%d ft" % (Pm // 2 - L),
                   ["%d ft" % (Pm - L), "%d ft" % (Pm - 2 * L), "%d ft" % (Pm // 2)],
                   "Two lengths: 2 × %d = %d. %d − %d = %d for the two widths. %d ÷ 2 = %d ft."
                   % (L, 2 * L, Pm, 2 * L, Pm - 2 * L, Pm - 2 * L, Pm // 2 - L), rnd))
    L, W = 25, 12
    its.append(mcq("A swimming pool is %d meters long and %d meters wide. A cover goes over the whole pool. "
                   "What is the area of the cover?" % (L, W), "%d sq m" % (L * W),
                   ["%d sq m" % (2 * (L + W)), "%d m" % (L * W), "%d sq m" % (L + W)],
                   area_e(L, W, "sq m") + " The cover spreads over the whole surface, so this is area.", rnd))
    n, he, his = P.next()
    L, W, door = 14, 11, 3
    Pm = 2 * (L + W)
    its.append(mcq("%s's room is %d feet long and %d feet wide. %s puts baseboard along the bottom of every wall, "
                   "except for a doorway that is %d feet wide. How much baseboard does %s need?"
                   % (n, L, W, cap(he), door, he), "%d ft" % (Pm - door),
                   ["%d ft" % Pm, "%d ft" % (L * W - door), "%d ft" % (L + W - door)],
                   "Perimeter: 2 × %d + 2 × %d = %d ft. No baseboard goes across the doorway: %d − %d = %d ft."
                   % (L, W, Pm, Pm, door, Pm - door), rnd))
    L, W = 45, 32
    its.append(mcq("A school playground is %d meters long and %d meters wide. What is its area?" % (L, W),
                   "%s sq m" % f(L * W), ["%d sq m" % (2 * (L + W)), "%s m" % f(L * W), "%d sq m" % no_zero(L, W)],
                   area_e(L, W, "sq m"), rnd))
    assert len(its) == 20, len(its)
    rnd.shuffle(its)
    return {"title": "L-shapes and word problems", "items": its}


# ------------------------------------------------------------ lesson
def ex(title, q, s, a):
    return ("<div class='sn-ex'><span class='sn-ex-t'>%s</span><p class='sn-ex-q'>%s</p>"
            "<p class='sn-ex-s'>%s</p><p class='sn-ex-a'>Answer: %s</p></div>" % (title, q, s, a))


def table(head, rows, cls="sn-table"):
    h = "".join("<th>%s</th>" % x for x in head)
    b = "".join("<tr>" + "".join("<td>%s</td>" % c for c in r) + "</tr>" for r in rows)
    return "<div class='sn-tw'><table class='%s'><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>" % (cls, h, b)


def body_html():
    return (
        "<h2>Two different questions</h2>"
        "<p><b>Area</b> is the space <b>inside</b> a shape, measured in square units (sq ft, sq m). "
        "<b>Perimeter</b> is the distance <b>around</b> it, measured in units of length (ft, m). "
        "For a rectangle, each one has a formula.</p>"
        "<h2>The two formulas</h2>"
        "<p><b>A = l × w</b> &nbsp;&nbsp; <b>P = 2 × l + 2 × w</b> (or 2 × (l + w))</p>"
        "<figure class='sn-fig'>" + rect_svg(12, 5, "12 ft", "5 ft", "rectangle 12 by 5") +
        "<figcaption>A = 12 × 5 = 60 sq ft. P = 2 × 12 + 2 × 5 = 24 + 10 = 34 ft.</figcaption></figure>" +
        ex("Example", "A rectangle is 24 m long and 15 m wide. Find the area and the perimeter.",
           "A = 24 × 15 = 360 (24 × 10 = 240, 24 × 5 = 120, 240 + 120 = 360). P = 2 × 24 + 2 × 15 = 48 + 30 = 78.",
           "360 sq m and 78 m") +
        "<h2>Find an unknown side</h2>"
        "<p>The area formula is a multiplication with a missing factor. Divide the area by the side you know.</p>"
        "<figure class='sn-fig'>" + rect_svg(9, 8, "9 ft", "? ft", "rectangle with area 72 and one unknown side",
                                             inside=["Area =", "72 sq ft"]) +
        "<figcaption>9 × ? = 72. 72 ÷ 9 = 8, so the width is 8 ft.</figcaption></figure>" +
        ex("From the perimeter", "A rectangle has a perimeter of 50 m. It is 15 m long. How wide is it?",
           "Two lengths: 2 × 15 = 30. 50 − 30 = 20 for the two widths. 20 ÷ 2 = 10.", "10 m") +
        "<h2>Area or perimeter?</h2>" +
        table(["The job", "Find", "Unit"], [
            ["Carpet, tiles, paint, grass", "Area (cover the inside)", "sq ft, sq m"],
            ["Fence, border, ribbon, trim", "Perimeter (go around the edge)", "ft, m, in"],
        ]) +
        "<h2>L-shapes</h2>"
        "<p>Split the shape into two rectangles and add their areas. Or find the big rectangle and subtract the missing corner.</p>"
        "<figure class='sn-fig'>" + l_svg(11, 9, 6, 4, "tr", ["5 m", "4 m", "6 m", "5 m", "11 m", "9 m"],
                                          "L-shaped figure split into two rectangles", split=True) +
        "<figcaption>5 × 9 = 45 and 6 × 5 = 30, so 45 + 30 = 75 sq m. Check: 11 × 9 − 6 × 4 = 99 − 24 = 75.</figcaption></figure>"
        "<h2>Common mistakes</h2>" +
        table(["Mistake", "What to do instead"], [
            ["P = l × w (12 × 5 = 60 ft)", "Perimeter adds all 4 sides: 2 × 12 + 2 × 5 = 34 ft"],
            ["Adding only two sides (12 + 5 = 17)", "A rectangle has 4 sides. Double the sum: 34"],
            ["Writing ft for an area", "Area is square units: 60 sq ft"],
            ["Perimeter 50, length 15: 50 − 15 = 35", "Take away both lengths, then halve: (50 − 30) ÷ 2 = 10"],
            ["L-shape area = big rectangle (11 × 9 = 99)", "Subtract the cut-out corner: 99 − 24 = 75"],
        ])
    )


FAQ = [
    {"q": "What are the area and perimeter formulas for a rectangle?",
     "a": "Area = length × width (A = l × w), in square units. Perimeter = 2 × length + 2 × width (P = 2l + 2w), in units of length."},
    {"q": "How do you find the missing side of a rectangle when you know the area?",
     "a": "Divide the area by the side you know. If the area is 72 sq ft and the length is 9 ft, the width is 72 ÷ 9 = 8 ft."},
    {"q": "How do you know whether a word problem is asking for area or perimeter?",
     "a": "If something covers the inside (carpet, tiles, paint, grass), find the area. If something goes around the edge (fence, border, ribbon, trim), find the perimeter."},
    {"q": "What does 4.MD.A.3 mean?",
     "a": "It is the Common Core Grade 4 standard for using the area and perimeter formulas for rectangles in real-world and math problems, including finding an unknown side length from the area or perimeter."},
]


def balance(sets, rnd):
    """Spread the correct answers evenly over the 4 positions in every set."""
    for s in sets:
        targets = [0, 1, 2, 3] * 5
        rnd.shuffle(targets)
        for it, t in zip(s["items"], targets):
            c = it["c"]
            c[it["a"]], c[t] = c[t], c[it["a"]]
            it["a"] = t


def mark_large(u, pattern):
    """Tag pictures that must print larger so their labels stay readable."""
    rx = re.compile(r"<svg (?=[^>]*aria-label='" + pattern + ")")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u


def gen_area_perimeter():
    rnd = random.Random(113)
    P = People(rnd)
    seen = set()
    sets = [set_formulas(rnd, seen), set_big(rnd, seen), set_unknown(rnd, seen), set_decide(rnd, P), set_story(rnd, P)]
    balance(sets, rnd)
    keys = set()
    for s in sets:
        assert len(s["items"]) == 20, (s["title"], len(s["items"]))
        for it in s["items"]:
            assert len(set(it["c"])) == 4, it
            k = it["q"] + "|" + "|".join(sorted(it["c"]))
            assert k not in keys, it["q"]
            keys.add(k)
    u = {
        "country": "us", "subject": "math", "grade": "grade-4", "slug": "area-perimeter-formulas", "sort": 13,
        "updated": UPDATED, "pdf_url": "",
        "title": "Area and Perimeter Formulas",
        "seo_title": "Grade 4 Area and Perimeter Worksheets: Formulas, Unknown Sides, L-Shapes and Word Problems",
        "short_title": "Area and perimeter formulas",
        "domain": "Measurement and Data",
        "standard_code": "4.MD.A.3",
        "standard_url": "https://www.thecorestandards.org/Math/Content/4/MD/A/3/",
        "standard_text": "Apply the area and perimeter formulas for rectangles in real world and mathematical problems. For example, find the width of a rectangular room given the area of the flooring and the length, by viewing the area formula as a multiplication equation with an unknown factor.",
        "meta_desc": "Free Grade 4 area and perimeter worksheets: use A = l × w and P = 2l + 2w, find an unknown side from the area or perimeter, choose area or perimeter, squares, L-shapes and real-world word problems. 100 practice questions with answers.",
        "key_big": "Area = length × width. Perimeter = 2 × length + 2 × width.",
        "key_sub": "Area covers the inside and is in square units (sq ft). Perimeter goes around the edge and is a length (ft). To find a missing side, divide the area by the side you know.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }
    return mark_large(u, "L-shaped figure")


if __name__ == "__main__":
    u = gen_area_perimeter()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
