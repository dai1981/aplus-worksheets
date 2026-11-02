# -*- coding: utf-8 -*-
"""
CA Grade 8 Math: The Pythagorean Theorem (Ontario Curriculum 2020, Spatial Sense E2.4)
  python3 tools/gen_caon_math_g8_pythagorean.py
Drawing engine (render) is copied from gen_caon_math_g6_area.py. Every figure is drawn to scale from its numbers.
Square roots are worked out exactly (fractions.Fraction) and rounded to the tenth with decimal.Decimal.
Canadian style: metric units, 4-digit numbers without a separator, 5 or more digits with a no-break space.
HTML attributes use single quotes (no backslashes in the JSON).
"""
import json, math, os, random, re
from decimal import Decimal, ROUND_HALF_UP, ROUND_DOWN, getcontext
from fractions import Fraction as Fr

getcontext().prec = 40
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "ca-on", "math", "grade-8")
UPDATED = "2026-11-02"
GREEN = "#006633"
FILL = "#cfe6d6"
SQFILL = "#eef6f0"
WHITE = "#ffffff"
RED = "#c0392b"
INK = "#2b2b2b"
GRAY = "#8a8a8a"
FONT = "Arial, Helvetica, sans-serif"
NBSP = " "
GIRLS = ["Olivia", "Emma", "Maya", "Zoe", "Amira", "Mei", "Chloe", "Priya", "Leah", "Hana", "Ava", "Sofia"]
BOYS = ["Liam", "Noah", "Aiden", "Lucas", "Owen", "Arjun", "Ethan", "Jayden", "Benjamin", "Mateo", "Nathan", "Kai"]


# ------------------------------------------------------------ numbers
def num(x):
    """Exact number as text, Ontario style: 4536, 14 096 (no-break space), 22.5."""
    x = Fr(x)
    assert x >= 0, x
    d = x.denominator
    while d % 2 == 0:
        d //= 2
    while d % 5 == 0:
        d //= 5
    assert d == 1, x
    s = format(Decimal(x.numerator) / Decimal(x.denominator), "f")
    if "." in s:
        s = s.rstrip("0").rstrip(".")
    i, _, fpart = s.partition(".")
    i = int(i)
    t = str(i) if i < 10000 else "{:,}".format(i).replace(",", NBSP)
    return t + ("." + fpart if fpart else "")


def F(x):
    return Fr(str(x))


def dtxt(d):
    """Decimal as text with grouping for 5+ digit whole parts."""
    s = format(d, "f")
    i, _, fp = s.partition(".")
    i = int(i)
    t = str(i) if i < 10000 else "{:,}".format(i).replace(",", NBSP)
    return t + ("." + fp if fp else "")


def exact_root(S):
    """√S as a Fraction when S is a perfect square, else None."""
    S = Fr(S)
    n, d = S.numerator, S.denominator
    rn, rd = math.isqrt(n), math.isqrt(d)
    if rn * rn == n and rd * rd == d:
        return Fr(rn, rd)
    return None


def dsqrt(S):
    S = Fr(S)
    return (Decimal(S.numerator) / Decimal(S.denominator)).sqrt()


def r1(S):
    """√S rounded to the nearest tenth (Decimal)."""
    return dsqrt(S).quantize(Decimal("0.1"), rounding=ROUND_HALF_UP)


def t1(S):
    """√S cut off (not rounded) after the tenths: a common rounding mistake."""
    return dsqrt(S).quantize(Decimal("0.1"), rounding=ROUND_DOWN)


def d3(S):
    return dsqrt(S).quantize(Decimal("0.001"), rounding=ROUND_DOWN)


def short(x):
    """A plain number (sum, difference, half) shown exactly when it has at most 1 decimal, else to the tenth."""
    x = Fr(x)
    if (x * 10).denominator == 1:
        return num(x)
    return dtxt((Decimal(x.numerator) / Decimal(x.denominator)).quantize(Decimal("0.1"), rounding=ROUND_HALF_UP))


def root_txt(S):
    """√S as text: exact, or rounded to the tenth."""
    e = exact_root(S)
    return num(e) if e is not None else dtxt(r1(S))


def L(x, u):
    return "%s %s" % (x, u)


def value_of(t):
    m = re.match(r"[\d" + NBSP + r".]+", t.lstrip("$"))
    if not m:
        return None
    return Decimal(m.group(0).replace(NBSP, ""))


# ------------------------------------------------------------ mcq
def mcq(q, correct, cands, e, rnd, by_value=True):
    """4 choices: correct + 3 unique distractors. With by_value, choices equal in value are skipped
    (5 cm and 5.0 cm), and so are zero or negative numbers."""
    correct = str(correct)
    seen_t = {correct}
    seen_v = set()
    v0 = value_of(correct) if by_value else None
    if v0 is not None:
        seen_v.add((v0, correct.split(" ", 1)[-1]))
    pick = []
    for c in cands:
        c = str(c)
        if c in seen_t or not c or c.startswith("-") or c.startswith("−"):
            continue
        if by_value:
            v = value_of(c)
            if v is not None:
                key = (v, c.split(" ", 1)[-1])
                if v == 0 or key in seen_v:
                    continue
                seen_v.add(key)
        seen_t.add(c)
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


def fig(svg):
    return "<div class='qfig'>" + svg + "</div>"


def svg_wrap(w, h, body, label):
    return ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 %d %d' width='%d' height='%d' "
            "role='img' aria-label='%s'><g font-family='%s'>%s</g></svg>" % (w, h, w, h, label, FONT, body))


def tw(t, fs):
    """Approximate width of bold Arial text in px. Periods and spaces are narrow."""
    t = str(t)
    return (len(t) - (t.count(",") + t.count(".")) * 0.6 - (t.count(" ") + t.count(NBSP)) * 0.3) * fs * 0.6


# ------------------------------------------------------------ drawing engine (from gen_caon_math_g6_area.py)
FS = 16
HH = 10


def seg_hits_box(p, q, b):
    x0, y0, x1, y1 = b
    dx, dy = q[0] - p[0], q[1] - p[1]
    t0, t1_ = 0.0, 1.0
    for pp, qq in ((-dx, p[0] - x0), (dx, x1 - p[0]), (-dy, p[1] - y0), (dy, y1 - p[1])):
        if pp == 0:
            if qq < 0:
                return False
        else:
            t = qq / pp
            if pp < 0:
                t0 = max(t0, t)
            else:
                t1_ = min(t1_, t)
            if t0 > t1_:
                return False
    return True


def inside(poly, x, y):
    n, c = len(poly), False
    for i in range(n):
        (x1, y1), (x2, y2) = poly[i], poly[(i + 1) % n]
        if (y1 > y) != (y2 > y) and x < x1 + (y - y1) * (x2 - x1) / (y2 - y1):
            c = not c
    return c


def render(polys, label, rights=(), labels=(), maxw=170, maxh=105):
    """Draw polygons to scale (y going up). rights = [(F, A, B)] right-angle marks.
    labels = [(p, q, text, polygon)] text outside the polygon next to segment pq.
    Returns None when the labels cannot be placed without touching a line."""
    allp = [p for pts, _ in polys for p in pts]
    x0, x1 = min(p[0] for p in allp), max(p[0] for p in allp)
    y0, y1 = min(p[1] for p in allp), max(p[1] for p in allp)
    k = min(maxw / (x1 - x0), maxh / (y1 - y0))

    def P(p):
        return ((p[0] - x0) * k, (y1 - p[1]) * k)
    segs, pp = [], []
    for pts, fill in polys:
        q = [P(p) for p in pts]
        pp.append((q, fill))
        segs += [(q[i], q[(i + 1) % len(q)]) for i in range(len(q))]
    marks = []
    for Fp, A, B in rights:
        Fp, A, B = P(Fp), P(A), P(B)
        u = (A[0] - Fp[0], A[1] - Fp[1])
        v = (B[0] - Fp[0], B[1] - Fp[1])
        lu, lv = math.hypot(*u), math.hypot(*v)
        s = 10
        a = (Fp[0] + u[0] / lu * s, Fp[1] + u[1] / lu * s)
        c = (Fp[0] + v[0] / lv * s, Fp[1] + v[1] / lv * s)
        m = (a[0] + c[0] - Fp[0], a[1] + c[1] - Fp[1])
        marks.append((a, m, c))
        segs += [(a, m), (m, c)]

    def clash(bx, boxes):
        for B in boxes:
            if bx[0] < B[2] + 8 and B[0] < bx[2] + 8 and bx[1] < B[3] + 5 and B[1] < bx[3] + 5:
                return True
        e = (bx[0] - 4, bx[1] - 3, bx[2] + 4, bx[3] + 3)
        return any(seg_hits_box(a, b, e) for a, b in segs)

    boxes, texts = [], []
    for a, b, t, mode in labels:
        a, b = P(a), P(b)
        dx, dy = b[0] - a[0], b[1] - a[1]
        Ln = math.hypot(dx, dy)
        n1 = (dy / Ln, -dx / Ln)
        poly = [P(p) for p in mode]
        mx, my = (a[0] + b[0]) / 2 + n1[0] * 2, (a[1] + b[1]) / 2 + n1[1] * 2
        sides = [(-n1[0], -n1[1]) if inside(poly, mx, my) else n1]
        hw = tw(t, FS) / 2
        done = False
        for fr in (0.5, 0.4, 0.6, 0.3, 0.7):
            for nx, ny in sides:
                off = 6 + abs(nx) * hw + abs(ny) * HH
                cx, cy = a[0] + dx * fr + nx * off, a[1] + dy * fr + ny * off
                bx = (cx - hw, cy - HH, cx + hw, cy + HH)
                if not clash(bx, boxes):
                    done = True
                    break
            if done:
                break
        if not done:
            return None
        boxes.append(bx)
        texts.append((cx, cy, t))
    xs = [p[0] for q, _ in pp for p in q] + [b[0] for b in boxes] + [b[2] for b in boxes]
    ys = [p[1] for q, _ in pp for p in q] + [b[1] for b in boxes] + [b[3] for b in boxes]
    pad = 5
    ox, oy = min(xs) - pad, min(ys) - pad
    W, H = int(math.ceil(max(xs) - ox + pad)), int(math.ceil(max(ys) - oy + pad))

    def pt(p):
        return "%.1f,%.1f" % (p[0] - ox, p[1] - oy)
    s = []
    for q, fill in pp:
        s.append("<polygon points='%s' fill='%s' stroke='%s' stroke-width='3' stroke-linejoin='round'/>"
                 % (" ".join(pt(p) for p in q), fill, GREEN))
    for a, m, c in marks:
        s.append("<polyline points='%s %s %s' fill='none' stroke='%s' stroke-width='1.8'/>" % (pt(a), pt(m), pt(c), INK))
    for cx, cy, t in texts:
        s.append("<text x='%.1f' y='%.1f' font-size='%d' font-weight='700' fill='%s' text-anchor='middle'>%s</text>"
                 % (cx - ox, cy - oy + 6, FS, RED if "?" in t else INK, t))
    return svg_wrap(W, H, "".join(s), label)


def must(svg):
    assert svg, "figure did not fit"
    return svg


# ------------------------------------------------------------ right triangles
def rot(p, deg):
    r = math.radians(deg)
    c, s = math.cos(r), math.sin(r)
    return (p[0] * c - p[1] * s, p[0] * s + p[1] * c)


def orient_angle(a, b, o):
    """Turns for a right triangle with the right angle C at the origin, leg a along x, leg b along y.
    0-3: legs across and up (the right angle in each corner); 4/5: hypotenuse flat at the bottom / top;
    6/7: hypotenuse standing up on the right / left; 8/9: tilted."""
    phi = math.degrees(math.atan2(b, -a))       # direction of the hypotenuse A -> B
    return [0, 90, 180, 270, 180 - phi, 360 - phi, 270 - phi, 90 - phi, 25, -30][o]


def tri_pts(a, b, o):
    a, b = float(a), float(b)
    d = orient_angle(a, b, o)
    C, A, B = (0.0, 0.0), (a, 0.0), (0.0, b)
    return [rot(p, d) for p in (C, A, B)]


def tri_svg(a, b, la, lb, lc, o, label="right triangle"):
    """Right triangle with legs a and b; la, lb, lc label leg a, leg b and the hypotenuse ('' for none)."""
    C, A, B = tri_pts(a, b, o)
    pts = [C, A, B]
    labels = []
    for p, q, t in ((C, A, la), (C, B, lb), (A, B, lc)):
        if t:
            labels.append((p, q, t, pts))
    return render([(pts, FILL)], label, rights=[(C, A, B)], labels=labels)


def tri_any(rnd, a, b, la, lb, lc, orients, label="right triangle"):
    os_ = list(orients)
    rnd.shuffle(os_)
    for o in os_:
        svg = tri_svg(a, b, la, lb, lc, o, label)
        if svg:
            return svg
    raise AssertionError(("no orientation fits", a, b, la, lb, lc))


def squares_svg(A1, A2, l1, l2, l3, mirror=False):
    """Right triangle (legs √A1 across and √A2 up) with a square drawn outward on each side.
    l1, l2, l3 are the labels inside the squares on leg 1, leg 2 and the hypotenuse."""
    a, b = math.sqrt(A1), math.sqrt(A2)
    sx = -1 if mirror else 1
    C, A, B = (0, 0), (a, 0), (0, b)
    sq1 = [C, A, (a, -a), (0, -a)]
    sq2 = [C, (-b, 0), (-b, b), B]
    sq3 = [A, B, (b, b + a), (a + b, a)]
    tri = [C, A, B]
    allp = sq1 + sq2 + sq3
    xs = [p[0] * sx for p in allp]
    ys = [p[1] for p in allp]
    ext = max(max(xs) - min(xs), max(ys) - min(ys))
    need = max(tw(l1, FS), tw(l2, FS)) + 14
    k = max(220.0 / ext, need / min(a, b), 30 / min(a, b))
    pad = 6
    x0, y1 = min(xs), max(ys)

    def P(p):
        return ((p[0] * sx - x0) * k + pad, (y1 - p[1]) * k + pad)
    W = int(math.ceil((max(xs) - min(xs)) * k + 2 * pad))
    H = int(math.ceil((max(ys) - min(ys)) * k + 2 * pad))
    assert W <= 300 and H <= 300, (A1, A2, W, H)
    s = []
    for poly, fill in ((sq1, SQFILL), (sq2, SQFILL), (sq3, SQFILL), (tri, FILL)):
        s.append("<polygon points='%s' fill='%s' stroke='%s' stroke-width='2.5' stroke-linejoin='round'/>"
                 % (" ".join("%.1f,%.1f" % P(p) for p in poly), fill, GREEN))
    # right-angle mark inside the triangle
    m = 10 / k
    s.append("<polyline points='%s' fill='none' stroke='%s' stroke-width='1.8'/>"
             % (" ".join("%.1f,%.1f" % P(p) for p in ((m, 0), (m, m), (0, m))), INK))
    for poly, t in ((sq1, l1), (sq2, l2), (sq3, l3)):
        cx = sum(p[0] for p in poly) / 4
        cy = sum(p[1] for p in poly) / 4
        X, Y = P((cx, cy))
        s.append("<text x='%.1f' y='%.1f' font-size='%d' font-weight='700' fill='%s' text-anchor='middle'>%s</text>"
                 % (X, Y + 6, FS, RED if "?" in t else INK, t))
    return svg_wrap(W, H, "".join(s), "right triangle with a square on each side")


def panels_svg(panels):
    """Four small right triangles A-D in one picture. panel = (a, b, orient, red) with red 0 = leg a, 1 = leg b,
    2 = hypotenuse. The red side is drawn thick and red."""
    cw, bw, bh, pad = 120, 96, 72, 8
    s = []
    for i, (a, b, o, red) in enumerate(panels):
        C, A, B = tri_pts(a, b, o)
        xs, ys = [p[0] for p in (C, A, B)], [p[1] for p in (C, A, B)]
        k = min(bw / (max(xs) - min(xs)), bh / (max(ys) - min(ys)))
        w, h = (max(xs) - min(xs)) * k, (max(ys) - min(ys)) * k
        ox = i * cw + pad + (cw - 2 * pad - w) / 2 + 4
        oy = pad + (bh - h) / 2

        def P(p):
            return ((p[0] - min(xs)) * k + ox, (max(ys) - p[1]) * k + oy)
        Cp, Ap, Bp = P(C), P(A), P(B)
        s.append("<polygon points='%s' fill='%s' stroke='%s' stroke-width='2.5' stroke-linejoin='round'/>"
                 % (" ".join("%.1f,%.1f" % p for p in (Cp, Ap, Bp)), FILL, GREEN))
        p, q = [(Cp, Ap), (Cp, Bp), (Ap, Bp)][red]
        s.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='6' stroke-linecap='round'/>"
                 % (p[0], p[1], q[0], q[1], RED))
        u = (Ap[0] - Cp[0], Ap[1] - Cp[1])
        v = (Bp[0] - Cp[0], Bp[1] - Cp[1])
        lu, lv = math.hypot(*u), math.hypot(*v)
        m1 = (Cp[0] + u[0] / lu * 10, Cp[1] + u[1] / lu * 10)
        m3 = (Cp[0] + v[0] / lv * 10, Cp[1] + v[1] / lv * 10)
        m2 = (m1[0] + m3[0] - Cp[0], m1[1] + m3[1] - Cp[1])
        s.append("<polyline points='%s' fill='none' stroke='%s' stroke-width='1.8'/>"
                 % (" ".join("%.1f,%.1f" % p for p in (m1, m2, m3)), INK))
        s.append("<text x='%.1f' y='%.1f' font-size='18' font-weight='700' fill='%s' text-anchor='middle'>%s</text>"
                 % (i * cw + cw / 2 + 4, pad + bh + 26, INK, "ABCD"[i]))
    return svg_wrap(4 * cw + 8, pad + bh + 34, "".join(s), "four right triangles A to D, one side of each in red")


# ------------------------------------------------------------ worked steps
def hyp_e(a, b, u):
    S = a * a + b * b
    e = "c² = %s² + %s² = %s + %s = %s. " % (num(a), num(b), num(a * a), num(b * b), num(S))
    r = exact_root(S)
    if r is not None:
        e += "c = √%s = %s %s." % (num(S), num(r), u)
    else:
        e += "c = √%s ≈ %s…, which rounds to %s %s." % (num(S), dtxt(d3(S))[:-1], dtxt(r1(S)), u)
    return e


def leg_e(c, a, u, x="b"):
    S = c * c - a * a
    e = "%s² = %s² − %s² = %s − %s = %s. " % (x, num(c), num(a), num(c * c), num(a * a), num(S))
    r = exact_root(S)
    if r is not None:
        e += "%s = √%s = %s %s." % (x, num(S), num(r), u)
    else:
        e += "%s = √%s ≈ %s…, which rounds to %s %s." % (x, num(S), dtxt(d3(S))[:-1], dtxt(r1(S)), u)
    return e


def hyp_cands(a, b, u):
    """Wrong answers for the hypotenuse, from real mistakes."""
    S = a * a + b * b
    c = [L(short(a + b), u)]                                 # added the legs without squaring
    if a != b:
        c.append(L(root_txt(abs(b * b - a * a)), u))         # subtracted instead of adding
    if exact_root(S) is None and t1(S) != r1(S):
        c.append(L(dtxt(t1(S)), u))                          # cut off instead of rounding
    c.append(L(short(S), u))                                 # forgot the square root
    c.append(L(short(S / 2), u))                             # halved instead of square root
    return c


def leg_cands(cc, a, u):
    S = cc * cc - a * a
    c = [L(root_txt(cc * cc + a * a), u)]                    # added instead of subtracting
    c.append(L(short(cc - a), u))                            # subtracted the sides without squaring
    if exact_root(S) is None and t1(S) != r1(S):
        c.append(L(dtxt(t1(S)), u))
    c.append(L(short(S), u))                                 # forgot the square root
    c.append(L(short(S / 2), u))
    return c


ROUND = " Round to the nearest tenth."


def hyp_q(q, a, b, u, rnd, extra=""):
    S = a * a + b * b
    if exact_root(S) is None:
        q += ROUND
    return mcq(q, L(root_txt(S), u), hyp_cands(a, b, u), hyp_e(a, b, u) + extra, rnd)


def leg_q(q, c, a, u, rnd, extra="", x="b"):
    S = c * c - a * a
    if exact_root(S) is None:
        q += ROUND
    return mcq(q, L(root_txt(S), u), leg_cands(c, a, u), leg_e(c, a, u, x) + extra, rnd)


# ------------------------------------------------------------ set 1: squares on the sides
def is_right(t):
    x, y, z = sorted(t)
    return x + y == z


def set_squares(rnd):
    its = []
    # 1) the two squares on the legs are given
    for i, (A1, A2, u) in enumerate([(9, 16, "cm"), (36, 64, "m"), (12, 13, "cm"), (20, 16, "m"),
                                     (18, 31, "cm"), (40, 24, "m")]):
        su = u + "²"
        S = A1 + A2
        svg = squares_svg(A1, A2, L(A1, su), L(A2, su), "?", mirror=i % 2 == 1)
        q = fig(svg) + "Squares are drawn on the sides of a right triangle. What is the area of the square on the hypotenuse?"
        e = ("The square on the hypotenuse equals the two smaller squares put together: %d + %d = %d %s."
             % (A1, A2, S, su))
        cands = [L(abs(A2 - A1), su)]
        r1_, r2_, r3_ = exact_root(A1), exact_root(A2), exact_root(S)
        if r3_ is not None:
            cands.append(L(num(r3_), su))
        cands.append(L(S, u))
        if r1_ is not None and r2_ is not None:
            cands += [L(num(r1_ + r2_), su), L(num((r1_ + r2_) ** 2), su)]
        if r3_ is not None:
            e += " (The hypotenuse itself is √%d = %s %s long.)" % (S, num(r3_), u)
        its.append(mcq(q, L(S, su), cands, e, rnd))
    # 2) the square on the hypotenuse and one leg are given
    for i, (H, A, u) in enumerate([(25, 9, "cm"), (100, 36, "m"), (41, 16, "cm"), (61, 25, "m"), (34, 9, "cm")]):
        su = u + "²"
        X = H - A
        if i % 2 == 0:
            svg = squares_svg(A, X, L(A, su), "?", L(H, su), mirror=i == 2)
        else:
            svg = squares_svg(X, A, "?", L(A, su), L(H, su), mirror=i == 3)
        q = fig(svg) + "Squares are drawn on the sides of a right triangle. What is the area of the square marked “?”"
        e = ("The two squares on the legs add up to the square on the hypotenuse: ? + %d = %d. "
             "So ? = %d − %d = %d %s." % (A, H, H, A, X, su))
        cands = [L(H + A, su)]
        rx = exact_root(X)
        if rx is not None:
            cands.append(L(num(rx), su))
        cands.append(L(X, u))
        rh, ra = exact_root(H), exact_root(A)
        if rh is not None and ra is not None:
            cands.append(L(num((rh - ra) ** 2), su))
        cands.append(L(Fr(H, 2), su))
        its.append(mcq(q, L(X, su), cands, e, rnd))
    # 3) from squares to sides and back
    q = "The square on the hypotenuse of a right triangle has an area of 169 cm². How long is the hypotenuse?"
    e = "The side of a square is the square root of its area: √169 = 13 cm, because 13 × 13 = 169."
    its.append(mcq(q, "13 cm", ["84.5 cm", "42.25 cm", "169 cm"], e, rnd))
    q = "The squares on the legs of a right triangle have areas of 36 m² and 64 m². How long is the hypotenuse?"
    e = "The square on the hypotenuse is 36 + 64 = 100 m². Its side is √100 = 10 m."
    its.append(mcq(q, "10 m", ["100 m", "14 m", "28 m"], e, rnd))
    q = "The legs of a right triangle are 5 cm and 12 cm. What is the area of the square on the hypotenuse?"
    e = "The squares on the legs are 5² = 25 cm² and 12² = 144 cm². The square on the hypotenuse is 25 + 144 = 169 cm²."
    its.append(mcq(q, "169 cm²", ["17 cm²", "289 cm²", "119 cm²"], e, rnd))
    q = ("A right triangle has a hypotenuse of 17 cm and one leg of 8 cm. "
         "What is the area of the square on the other leg?")
    e = "Square on the hypotenuse: 17² = 289 cm². Square on the known leg: 8² = 64 cm². Other square: 289 − 64 = 225 cm²."
    its.append(mcq(q, "225 cm²", ["353 cm²", "81 cm²", "9 cm²"], e, rnd))
    # 4) which squares fit a right triangle?
    for right, wrongs in [((25, 144, 169), [(25, 144, 196), (5, 12, 13), (16, 25, 36)]),
                          ((64, 225, 289), [(8, 15, 17), (64, 225, 256), (49, 64, 121)]),
                          ((20, 30, 50), [(20, 30, 40), (16, 36, 49), (25, 36, 64)])]:
        assert is_right(right) and not any(is_right(w) for w in wrongs)

        def tx(t):
            return "%d, %d and %d" % t
        q = ("Each choice gives the areas of three squares, in cm². Which three squares could be drawn on the sides "
             "of a right triangle?")
        e = ("The two smaller areas must add up to the largest: %d + %d = %d. "
             "Check the others: %s." % (right[0], right[1], right[2],
                                        "; ".join("%d + %d = %d, not %d" % (w[0], w[1], w[0] + w[1], w[2]) for w in wrongs)))
        its.append(mcq(q, tx(right), [tx(w) for w in wrongs], e, rnd, by_value=False))
    # 5) is it a right triangle?
    q = "A triangle has sides of 6 cm, 8 cm and 10 cm. Is it a right triangle?"
    e = "Square the sides: 6² + 8² = 36 + 64 = 100, and 10² = 100. They match, so it is a right triangle."
    its.append(mcq(q, "Yes: 36 + 64 = 100", ["No: 6 + 8 ≠ 10", "No: 64 − 36 ≠ 10", "Yes: 6 + 8 > 10"], e, rnd,
                   by_value=False))
    q = "A triangle has sides of 7 cm, 8 cm and 11 cm. Is it a right triangle?"
    e = ("Square the sides: 7² + 8² = 49 + 64 = 113, but 11² = 121. They do not match, so it is not a right triangle "
         "(its largest angle is a little more than 90°).")
    its.append(mcq(q, "No: 49 + 64 ≠ 121", ["Yes: 7 + 8 > 11", "Yes: 49 + 64 > 11", "Yes: 8 + 11 > 7"], e, rnd,
                   by_value=False))
    assert len(its) == 20, len(its)
    return {"title": "Squares on the sides: the area model", "items": its}


# ------------------------------------------------------------ set 2: identify the hypotenuse
SMALL = [(3, 4), (4, 3), (5, 6), (6, 5), (1, 1), (4, 5), (5, 4), (2, 3), (3, 2), (5, 7)]


def set_identify(rnd):
    its = []
    # 1) four pictures: in which one is the red side the hypotenuse?
    answers = [0, 1, 2, 3, rnd.randrange(4)]
    for ans in answers:
        panels = []
        for j in range(4):
            a, b = rnd.choice(SMALL)
            if j == ans:
                o = rnd.choice([4, 5, 6, 7, 8, 9])
                red = 2
            else:
                o = rnd.choice([0, 1, 2, 3, 4, 5, 8, 9])
                red = rnd.choice([0, 1])
            panels.append((a, b, o, red))
        # at least one wrong picture shows a red leg lying flat, at least one shows a red leg that is slanted
        q = fig(panels_svg(panels)) + "In which triangle is the red side the hypotenuse?"
        e = ("The hypotenuse is the side opposite the right angle (the small square). In triangle %s the red side "
             "is across from the right angle. In the others the red side touches the right angle, so it is a leg."
             % "ABCD"[ans])
        its.append({"q": q, "c": ["A", "B", "C", "D"], "a": ans, "e": e, "_fixed": True})
    # 2) letters on the sides: which equation is true?
    letters = [("x", "y", "z"), ("p", "q", "r"), ("a", "b", "c"), ("m", "n", "k"), ("d", "e", "f"), ("s", "t", "w")]
    tris = [(3, 4), (5, 12), (8, 6), (12, 9), (15, 8), (4, 5)]
    orients = [0, 4, 1, 6, 5, 9]
    for i in range(6):
        l = list(letters[i])
        if l == ["a", "b", "c"]:
            h, l1, l2 = "a", "b", "c"
        else:
            rnd.shuffle(l)
            l1, l2, h = l
        a, b = tris[i]
        svg = tri_any(rnd, a, b, l1, l2, h, [orients[i]], "right triangle with letters on its sides")
        q = fig(svg) + "Which equation is true for this right triangle?"
        right = "%s² + %s² = %s²" % (l1, l2, h)
        e = ("The hypotenuse is %s, the side opposite the right angle. The squares of the two legs add up to the square "
             "of the hypotenuse: %s." % (h, right))
        if h != "c":
            pass
        if h == "a":
            e += " The letters do not matter: here the hypotenuse is called a."
        its.append(mcq(q, right, ["%s² + %s² = %s²" % (l1, h, l2), "%s² + %s² = %s²" % (l2, h, l1),
                                  "%s + %s = %s" % (l1, l2, h)], e, rnd, by_value=False))
    # 3) the hypotenuse lies flat or stands up: how long is it?
    for (a, b, c, u), o in zip([(9, 12, 15, "cm"), (10, 24, 26, "m"), (12, 16, 20, "cm")], [4, 6, 5]):
        svg = must(tri_svg(a, b, L(a, u), L(b, u), L(c, u), o, "right triangle with all three sides labelled"))
        q = fig(svg) + "How long is the hypotenuse of this right triangle?"
        e = ("The hypotenuse is opposite the right angle, and it is always the longest side: %d %s. "
             "Check: %d² + %d² = %d + %d = %d = %d²." % (c, u, a, b, a * a, b * b, c * c, c))
        its.append(mcq(q, L(c, u), [L(a, u), L(b, u), L(a + b, u)], e, rnd))
    # 4) three lengths in words
    for a, b, c, u in [(20, 21, 29, "cm"), (Fr(6, 10), Fr(8, 10), 1, "m")]:
        q = "A right triangle has sides of %s %s, %s %s and %s %s. Which length is the hypotenuse?" % (
            num(b), u, num(c), u, num(a), u)
        e = ("The hypotenuse is the longest side of a right triangle: %s %s. Check: %s² + %s² = %s + %s = %s = %s²."
             % (num(c), u, num(a), num(b), num(a * a), num(b * b), num(c * c), num(c)))
        its.append(mcq(q, L(num(c), u), [L(num(a), u), L(num(b), u), "You cannot tell without a picture."], e, rnd))
    # 5) what the hypotenuse is
    q = "In a right triangle, the hypotenuse is the side that is …"
    e = "The hypotenuse is across from (opposite) the right angle. The two sides that form the right angle are the legs."
    its.append(mcq(q, "opposite the right angle", ["next to the right angle", "at the bottom of the triangle",
                                                   "the shortest side"], e, rnd, by_value=False))
    q = "Which statement about the hypotenuse of a right triangle is always true?"
    e = ("The hypotenuse is always the longest side, because its square equals the squares of both legs added together. "
         "It can be drawn in any direction, and it is shorter than the two legs added together.")
    its.append(mcq(q, "It is the longest side.", ["It is the side at the bottom.", "It equals the two legs added.",
                                                  "It is shorter than one leg."], e, rnd, by_value=False))
    # 6) equation for given lengths
    for a, b, c in [(7, 24, 25), (9, 40, 41)]:
        q = "A right triangle has legs of %d cm and %d cm and a hypotenuse of %d cm. Which equation shows the Pythagorean relationship?" % (a, b, c)
        e = "Legs squared and added equal the hypotenuse squared: %d² + %d² = %d + %d = %d = %d²." % (a, b, a * a, b * b, c * c, c)
        its.append(mcq(q, "%d² + %d² = %d²" % (a, b, c), ["%d² + %d² = %d²" % (a, c, b), "%d² + %d² = %d²" % (b, c, a),
                                                          "%d + %d = %d" % (a, b, c)], e, rnd, by_value=False))
    assert len(its) == 20, len(its)
    return {"title": "Identify the hypotenuse", "items": its}


# ------------------------------------------------------------ set 3: find the hypotenuse
ALL_O = list(range(10))


def set_hyp(rnd):
    its = []
    for i, (a, b, u) in enumerate([(3, 4, "cm"), (6, 8, "m"), (5, 12, "cm"), (8, 15, "m"), (9, 12, "cm"),
                                   (20, 21, "m"), (12, 16, "cm"), (10, 24, "m")]):
        svg = tri_any(rnd, a, b, L(a, u), L(b, u), "?", ALL_O)
        its.append(hyp_q(fig(svg) + "Find the length of the hypotenuse.", F(a), F(b), u, rnd))
    for a, b, u in [(4, 7, "cm"), (5, 9, "m"), (6, 10, "cm"), (7, 12, "m")]:
        assert exact_root(a * a + b * b) is None and t1(a * a + b * b) != r1(a * a + b * b), (a, b)
        svg = tri_any(rnd, a, b, L(a, u), L(b, u), "?", ALL_O)
        its.append(hyp_q(fig(svg) + "Find the length of the hypotenuse.", F(a), F(b), u, rnd))
    for a, b, u in [("1.5", "2", "m"), ("0.9", "1.2", "m"), (30, 40, "cm"), (24, 45, "cm")]:
        a, b = F(a), F(b)
        its.append(hyp_q("The legs of a right triangle are %s %s and %s %s. How long is the hypotenuse?"
                         % (num(a), u, num(b), u), a, b, u, rnd))
    for a, b, u in [("2.5", "4", "m"), (11, 14, "cm")]:
        a, b = F(a), F(b)
        its.append(hyp_q("The legs of a right triangle are %s %s and %s %s. How long is the hypotenuse?"
                         % (num(a), u, num(b), u), a, b, u, rnd))
    for a, b in [(6, 9), (8, 13)]:
        q = "A right triangle has legs of %d cm and %d cm. Which calculation gives the length of the hypotenuse?" % (a, b)
        right = "√(%d² + %d²)" % (a, b)
        e = ("Square the legs, add, then take the square root: %s = √(%d + %d) = √%d ≈ %s cm. "
             "%d² + %d² without the square root is the area of the square on the hypotenuse, not its side."
             % (right, a * a, b * b, a * a + b * b, dtxt(r1(a * a + b * b)), a, b))
        its.append(mcq(q, right, ["√(%d² − %d²)" % (b, a), "%d + %d" % (a, b), "%d² + %d²" % (a, b)], e, rnd,
                       by_value=False))
    assert len(its) == 20, len(its)
    return {"title": "Find the hypotenuse", "items": its}


# ------------------------------------------------------------ set 4: find a leg
def set_leg(rnd):
    its = []
    for c, a, u in [(5, 4, "cm"), (13, 5, "m"), (17, 15, "cm"), (10, 8, "m"), (25, 7, "cm"), (29, 21, "m"),
                    (15, 12, "cm"), (34, 30, "m")]:
        b = exact_root(c * c - a * a)
        assert b is not None
        svg = tri_any(rnd, a, b, L(a, u), "?", L(c, u), ALL_O)
        its.append(leg_q(fig(svg) + "Find the length of the missing leg.", F(c), F(a), u, rnd))
    for c, a, u in [(9, 5, "cm"), (13, 7, "m"), (11, 5, "cm"), (8, 6, "m")]:
        S = c * c - a * a
        assert exact_root(S) is None and t1(S) != r1(S), (c, a, d3(S))
        svg = tri_any(rnd, a, math.sqrt(S), L(a, u), "?", L(c, u), ALL_O)
        its.append(leg_q(fig(svg) + "Find the length of the missing leg.", F(c), F(a), u, rnd))
    for c, a, u in [("2.5", "1.5", "m"), ("6.5", "2.5", "m"), (50, 14, "cm"), (61, 11, "cm")]:
        c, a = F(c), F(a)
        its.append(leg_q("A right triangle has a hypotenuse of %s %s and one leg of %s %s. How long is the other leg?"
                         % (num(c), u, num(a), u), c, a, u, rnd))
    for c, a, u in [(10, 7, "cm"), ("4.5", "2", "m")]:
        c, a = F(c), F(a)
        its.append(leg_q("A right triangle has a hypotenuse of %s %s and one leg of %s %s. How long is the other leg?"
                         % (num(c), u, num(a), u), c, a, u, rnd))
    for c, a in [(15, 9), (20, 11)]:
        q = ("A right triangle has a hypotenuse of %d cm and one leg of %d cm. "
             "Which calculation gives the length of the other leg?" % (c, a))
        right = "√(%d² − %d²)" % (c, a)
        S = c * c - a * a
        e = ("Square both, subtract the leg from the hypotenuse, then take the square root: %s = √(%d − %d) = √%d %s %s cm. "
             "Adding the squares only works when you are finding the hypotenuse."
             % (right, c * c, a * a, S, "=" if exact_root(S) is not None else "≈", root_txt(S)))
        its.append(mcq(q, right, ["√(%d² + %d²)" % (c, a), "%d − %d" % (c, a), "%d² − %d²" % (c, a)], e, rnd,
                       by_value=False))
    assert len(its) == 20, len(its)
    return {"title": "Find a missing leg", "items": its}


# ------------------------------------------------------------ set 5: word problems
def set_story(rnd, P):
    its = []
    LEGNOTE = " (Adding the squares gives a length longer than the hypotenuse, which is impossible for a leg.)"
    n, he, his = P.next()
    its.append(leg_q("A 5 m ladder leans against the wall of %s’s cottage. Its foot is 1.2 m from the wall. "
                     "How high up the wall does the ladder reach?" % n, F(5), F("1.2"), "m", rnd,
                     " The ladder is the hypotenuse; the ground and the wall are the legs.", x="h"))
    n, he, his = P.next()
    its.append(hyp_q("%s leans a ladder against a wall so that it reaches 3.6 m up the wall. The foot of the ladder is "
                     "1.5 m from the wall. How long is the ladder?" % n, F("3.6"), F("1.5"), "m", rnd,
                     " The ladder is opposite the right angle between the wall and the ground."))
    its.append(hyp_q("A wheelchair ramp at a community centre rises 0.5 m over a horizontal distance of 6 m. "
                     "How long is the sloping surface of the ramp?", F("0.5"), F(6), "m", rnd))
    n, he, his = P.next()
    its.append(hyp_q("%s builds a skateboard ramp that is 0.7 m high and 2.4 m long along the ground. "
                     "How long is the sloping top of the ramp?" % n, F("0.7"), F("2.4"), "m", rnd))
    its.append(hyp_q("A park in Ottawa is a rectangle 120 m long and 50 m wide. A path goes straight across it from one "
                     "corner to the opposite corner. How long is the path?", F(120), F(50), "m", rnd))
    n, he, his = P.next()
    q = ("A rectangular park is 80 m long and 60 m wide. %s walks along two sides to get to the opposite corner. "
         "%s friend takes the diagonal path. How much shorter is the diagonal path?" % (n, his.capitalize()))
    e = ("Diagonal: √(80² + 60²) = √(6400 + 3600) = √%s000 = 100 m. Along the sides: 80 + 60 = 140 m. "
         "Difference: 140 − 100 = 40 m." % ("10" + NBSP))
    its.append(mcq(q, "40 m", ["100 m", "140 m", "20 m"], e, rnd))
    its.append(hyp_q("A TV screen is 96 cm wide and 54 cm tall. TV sizes are measured along the diagonal of the screen. "
                     "How long is the diagonal?", F(96), F(54), "cm", rnd))
    its.append(hyp_q("A tablet screen is 24 cm wide and 18 cm tall. How long is its diagonal?", F(24), F(18), "cm", rnd))
    its.append(leg_q("An older TV has a screen with a 100 cm diagonal. The screen is 80 cm wide. How tall is it?",
                     F(100), F(80), "cm", rnd, x="h"))
    its.append(hyp_q("A soccer field is 100 m long and 64 m wide. How far is it from one corner flag to the opposite "
                     "corner flag, in a straight line?", F(100), F(64), "m", rnd))
    its.append(hyp_q("An NHL hockey rink is about 61 m long and 26 m wide. About how far is it diagonally from one "
                     "corner to the opposite corner?", F(61), F(26), "m", rnd))
    n, he, his = P.next()
    its.append(hyp_q("On a canoe trip, %s paddles 1.2 km north and then 0.5 km east across a lake. How far is %s from "
                     "the starting point, in a straight line?" % (n, he), F("1.2"), F("0.5"), "km", rnd))
    its.append(hyp_q("A wire runs from a point 8 m up a flagpole to a stake in the ground 6 m from the bottom of the "
                     "pole. How long is the wire?", F(8), F(6), "m", rnd))
    n, he, his = P.next()
    its.append(leg_q("%s flies a kite on a 50 m string. The kite is right above a point on the ground 30 m away from %s. "
                     "How high is the kite? (Ignore %s height.)" % (n, "her" if he == "she" else "him", his),
                     F(50), F(30), "m", rnd, " The string is the hypotenuse.", x="h"))
    its.append(hyp_q("The bases on a baseball diamond form a square with sides of 27.4 m. How far does the catcher "
                     "throw from home plate straight to second base?", F("27.4"), F("27.4"), "m", rnd,
                     " Home plate, first base and second base make a right triangle."))
    its.append(hyp_q("A window is 6 m above the ground. For safety, the foot of a ladder must be 1.5 m from the wall. "
                     "How long must the ladder be to reach the window?", F(6), F("1.5"), "m", rnd))
    n, he, his = P.next()
    its.append(hyp_q("%s hikes 2.4 km east and then 1.8 km north in Algonquin Park. How far is %s from the trailhead, "
                     "in a straight line?" % (n, he), F("2.4"), F("1.8"), "km", rnd))
    its.append(hyp_q("A garden gate is 1.2 m wide and 1 m tall. A wooden brace goes from one corner to the opposite "
                     "corner. How long is the brace?", F("1.2"), F(1), "m", rnd))
    its.append(leg_q("A 3 m ramp goes from the back of a moving truck to the ground. The back of the truck is 0.9 m "
                     "high. How far from the truck does the ramp touch the ground?", F(3), F("0.9"), "m", rnd,
                     " The ramp is the hypotenuse.", x="d"))
    its.append(hyp_q("A square schoolyard is 40 m on each side. How long is a path straight across it from one corner to "
                     "the opposite corner?", F(40), F(40), "m", rnd))
    assert len(its) == 20, len(its)
    return {"title": "Word problems: ladders, ramps, parks and screens", "items": its}


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
        "<h2>Legs and hypotenuse</h2>"
        "<p>A right triangle has one 90° angle, shown with a small square. "
        "The two sides that form the right angle are the <b>legs</b> (a and b). "
        "The side opposite the right angle is the <b>hypotenuse</b> (c). It is always the longest side, "
        "and it can point in any direction.</p>"
        "<figure class='sn-fig'>" + must(tri_svg(4, 3, "a", "b", "c (hypotenuse)", 0, "right triangle with legs a and b and hypotenuse c")) +
        "<figcaption>The hypotenuse c is across from the right angle.</figcaption></figure>"
        "<h2>The area model: a² + b² = c²</h2>"
        "<p>Draw a square on each side of a right triangle. The two squares on the legs together have exactly the same "
        "area as the square on the hypotenuse. This is the <b>Pythagorean theorem</b>.</p>"
        "<figure class='sn-fig'>" + squares_svg(9, 16, "9", "16", "25") +
        "<figcaption>Legs 3 and 4: 3² + 4² = 9 + 16 = 25 = 5². The hypotenuse is 5.</figcaption></figure>"
        "<p>It only works for right triangles. It also works the other way: if a² + b² = c², the triangle has a right angle.</p>"
        "<h2>Find the hypotenuse: add the squares</h2>"
        "<p>Square the two legs, add, then take the square root.</p>" +
        ex("Example", "The legs are 6 cm and 8 cm. Find the hypotenuse.",
           "c² = 6² + 8² = 36 + 64 = 100. c = √100 = 10.", "10 cm") +
        ex("Round at the end", "The legs are 4 cm and 7 cm. Find the hypotenuse to the nearest tenth.",
           "c² = 16 + 49 = 65. c = √65 ≈ 8.06, which rounds to 8.1.", "8.1 cm") +
        "<h2>Find a leg: subtract the squares</h2>"
        "<p>Square the hypotenuse and the known leg, subtract, then take the square root.</p>"
        "<figure class='sn-fig'>" + must(tri_svg(5, 12, "5 cm", "?", "13 cm", 0, "right triangle with a missing leg")) +
        "<figcaption>b² = 13² − 5² = 169 − 25 = 144, so b = √144 = 12 cm.</figcaption></figure>"
        "<p>A leg is always shorter than the hypotenuse. If your answer is longer, you added instead of subtracting.</p>"
        "<h2>Pythagorean triples</h2>"
        "<p>Some right triangles have three whole-number sides. Multiples of a triple are triples too (6, 8, 10).</p>" +
        table(["Legs", "Hypotenuse", "Check"], [
            ["3 and 4", "5", "9 + 16 = 25"],
            ["5 and 12", "13", "25 + 144 = 169"],
            ["8 and 15", "17", "64 + 225 = 289"],
            ["7 and 24", "25", "49 + 576 = 625"],
        ]) +
        "<h2>Common mistakes</h2>" +
        table(["Mistake", "What to do instead"], [
            ["Adding the sides: 3 + 4 = 7", "Square first: 3² + 4² = 25, so c = 5"],
            ["Subtracting to find the hypotenuse", "Hypotenuse: add the squares. Leg: subtract"],
            ["Stopping at c² = 25", "Take the square root: c = 5"],
            ["Calling the bottom side the hypotenuse", "Find the side opposite the right angle"],
            ["Rounding before the last step", "Round only the final square root"],
        ])
    )


FAQ = [
    {"q": "Is the Pythagorean theorem taught in Grade 8 in Ontario?",
     "a": "Yes. In the Grade 8 Ontario math curriculum (Spatial Sense, E2.4), students describe the Pythagorean relationship with geometric models such as squares on the sides, and use it to find an unknown side of a right triangle."},
    {"q": "How do you know which side is the hypotenuse?",
     "a": "The hypotenuse is the side opposite the right angle, and it is always the longest side. The two sides that form the right angle are the legs."},
    {"q": "How do you find a missing leg with the Pythagorean theorem?",
     "a": "Subtract instead of add: square the hypotenuse and the known leg, subtract, then take the square root. For example, √(13² − 5²) = √144 = 12."},
    {"q": "What is a Pythagorean triple?",
     "a": "Three whole numbers that fit a² + b² = c², such as 3, 4, 5 or 5, 12, 13. Any multiple, like 6, 8, 10, is also a triple."},
]


def balance(sets, rnd):
    """Spread the correct answers evenly (5 per position). Picture questions (A-D) keep their order."""
    for s in sets:
        need = [5, 5, 5, 5]
        for it in s["items"]:
            if it.get("_fixed"):
                need[it["a"]] -= 1
        targets = [i for i in range(4) for _ in range(need[i])]
        assert min(need) >= 0
        rnd.shuffle(targets)
        free = [it for it in s["items"] if not it.get("_fixed")]
        assert len(free) == len(targets)
        for it, t in zip(free, targets):
            c = it["c"]
            c[it["a"]], c[t] = c[t], c[it["a"]]
            it["a"] = t
        for it in s["items"]:
            it.pop("_fixed", None)


def mark_large(u, pattern):
    rx = re.compile(r"<svg (?=[^>]*aria-label='" + pattern + ")")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u


def gen():
    rnd = random.Random(48817)
    P = People(rnd)
    sets = [set_squares(rnd), set_identify(rnd), set_hyp(rnd), set_leg(rnd), set_story(rnd, P)]
    for s in sets:
        rnd.shuffle(s["items"])
    balance(sets, rnd)
    keys = set()
    for s in sets:
        assert len(s["items"]) == 20, (s["title"], len(s["items"]))
        assert [sum(1 for it in s["items"] if it["a"] == i) for i in range(4)] == [5, 5, 5, 5], s["title"]
        for it in s["items"]:
            assert len(set(it["c"])) == 4, it
            assert it["e"], it
            assert it["q"].count("<svg") <= 1
            k = it["q"] + "|" + "|".join(sorted(it["c"]))
            assert k not in keys, it["q"]
            keys.add(k)
            for x in [it["q"], it["e"]] + it["c"]:
                assert not re.search(r"\d,\d{3}", re.sub(r"<svg.*?</svg>", "", x)), x
                assert not re.search(r"\d \d{3}", re.sub(r"<svg.*?</svg>", "", x)), x
    u = {
        "country": "ca-on", "subject": "math", "grade": "grade-8", "slug": "pythagorean-theorem", "sort": 17,
        "updated": UPDATED, "pdf_url": "",
        "title": "The Pythagorean Theorem: Squares on the Sides, the Hypotenuse and Missing Legs",
        "seo_title": "Grade 8 Pythagorean Theorem Worksheets: Find the Hypotenuse and a Missing Side (Free, Answer Key)",
        "short_title": "Pythagorean theorem",
        "domain": "Spatial Sense",
        "standard_code": "Grade 8: E2.4",
        "standard_url": "https://www.dcp.edu.gov.on.ca/en/curriculum/elementary-mathematics",
        "standard_text": "Describe the Pythagorean relationship using various geometric models, and apply the theorem to solve problems involving an unknown side length for a given right triangle",
        "meta_desc": "Free Grade 8 math worksheets on the Pythagorean theorem for the Ontario curriculum: the area model with squares on the sides, identifying the hypotenuse, finding the hypotenuse or a missing leg (rounded to the nearest tenth), and word problems with ladders, ramps, parks and TV screens. 100 questions with an answer key.",
        "key_big": "a² + b² = c²",
        "key_sub": "In a right triangle, the square on the hypotenuse c (the side opposite the right angle) equals the squares on the two legs added together. To find the hypotenuse, add the squares and take the square root. To find a leg, subtract the squares and take the square root.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }
    return mark_large(u, "(?:right triangle with a square on each side|four right triangles)")


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
