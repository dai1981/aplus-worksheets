# -*- coding: utf-8 -*-
"""
Philippines Grade 4 Math (MATATAG): Reflection and Glide Reflection (Grade 4: Measurement and Geometry)
  python3 tools/gen_ph_math_g4_reflection.py
Finding the image of a point after a reflection and after a glide reflection, checking a reflected shape, and naming
the move from shape A to shape B (own makers on the UK Year 5 grid), and translations (UK Year 5 maker).
Wrong answers come from real mistakes: putting the image the wrong distance from the line, sliding instead of
flipping, and forgetting the slide in a glide reflection.
"""
import ph_common
from ph_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example, peso, words)
import random
import gen_uk_maths_y5_reflection_translation as ukt
adopt(ukt)
if hasattr(ukt, 'R'): ukt.R = random.Random(704200)
ph_common.GRADE = "grade-4"

def uniq(fn):
    """Never give the same question twice, even with other wrong answers."""
    seen = set()
    def f(r):
        it = fn(r)
        if it is None or it["q"] in seen:
            raise AssertionError("repeat")
        seen.add(it["q"])
        return it
    f.__name__ = fn.__name__
    return f


import gen_uk_maths_y5_reflection_translation as ukr
from gen_uk_maths_y5_reflection_translation import Grid, reflect, shift
from ws_common import GREEN, RED
BLUE = ukr.BLUE
LET = ["A", "B", "C", "D"]
mcq_fixed = ukr.mcq_fixed

SHAPES = [[(0, 0), (3, 0), (0, 2)], [(0, 0), (2, 0), (2, 1), (1, 1), (1, 3), (0, 3)], [(0, 0), (3, 0), (2, 2), (0, 2)],
          [(0, 0), (1, 0), (1, 2), (2, 2), (2, 3), (0, 3)], [(0, 0), (3, 0), (3, 1), (1, 1), (1, 2), (0, 2)], [(0, 0), (2, 0), (0, 3)],
          [(0, 0), (3, 1), (0, 2)]]


def place(shape, dx, dy):
    return shift(shape, dx, dy)


def bbox(p):
    return min(x for x, y in p), max(x for x, y in p), min(y for x, y in p), max(y for x, y in p)


def fits(p, nx, ny):
    a, b, c, d = bbox(p)
    return a >= 0 and c >= 0 and b <= nx and d <= ny


def asym(shape):
    """reflected shape must look different from a slide of the shape"""
    m = [reflect(p, ("v", 0)) for p in shape]
    a = bbox(m)
    m = sorted(shift(m, -a[0], -a[2]))
    b = bbox(shape)
    s = sorted(shift(shape, -b[0], -b[2]))
    mh = [reflect(p, ("h", 0)) for p in shape]
    c = bbox(mh)
    mh = sorted(shift(mh, -c[0], -c[2]))
    return m != s and mh != s


SH = [s for s in SHAPES if asym(s)]


def one_point(r, glide=False):
    kind = r.choice(["v", "h"])
    nx, ny = 10, 8
    m = r.randint(4, 6) if kind == "v" else r.randint(3, 5)
    for _ in range(200):
        p = (r.randint(1, m - 1), r.randint(1, ny - 1)) if kind == "v" else (r.randint(1, nx - 1), r.randint(1, m - 1))
        k = r.randint(2, 3) * r.choice([1, -1])
        img = reflect(p, (kind, m))
        if glide:
            img = (img[0], img[1] + k) if kind == "v" else (img[0] + k, img[1])
        along = (lambda q, d: (q[0], q[1] + d)) if kind == "v" else (lambda q, d: (q[0] + d, q[1]))
        across = (lambda q, d: (q[0] + d, q[1])) if kind == "v" else (lambda q, d: (q[0], q[1] + d))
        refl = reflect(p, (kind, m))
        if glide:
            cand = [img, refl, along(refl, -k), along(p, k)]
        else:
            s2 = r.choice([2, -2])
            cand = [img, across(img, 2), along(img, s2), across(along(img, -s2), 2)]
        if len(set(cand + [p])) == 5 and all(0 < c[0] < nx and 0 < c[1] < ny for c in cand) and all(c[0] != m if kind == "v" else c[1] != m for c in cand):
            break
    else:
        raise AssertionError
    order = cand[:]
    r.shuffle(order)
    ans = LET[order.index(img)]
    G = Grid(nx, ny)
    G.mirror(kind, m)
    G.point(p[0], p[1], "P", RED)
    for i, c in enumerate(order):
        G.point(c[0], c[1], LET[i])
    side = "left" if kind == "v" else "below"
    dist = (m - p[0]) if kind == "v" else (m - p[1])
    sq = lambda n: "%d square%s" % (n, "" if n == 1 else "s")
    if glide:
        move = ("%d squares %s" % (abs(k), "up" if k > 0 else "down")) if kind == "v" else ("%d squares %s" % (abs(k), "right" if k > 0 else "left"))
        q = "Point P is reflected in the dashed line, then slid %s along the line. This is a glide reflection. Which point is the image of P?" % move
        e = "P is %s from the line, so its reflection is %s from the line on the other side. Then slide it %s. That is point <b>%s</b>." % (sq(dist), sq(dist), move, ans)
    else:
        q = "Point P is reflected in the dashed line. Which point is the image of P?"
        e = "P is %s from the line, so the image is %s from the line on the other side, straight across. That is point <b>%s</b>." % (sq(dist), sq(dist), ans)
    return mcq_fixed(fig(G.svg("grid with a dashed mirror line, point P and points A to D")) + q, LET, ans, e)


def one_glide_pt(r):
    return one_point(r, glide=True)


WHAT = ["a reflection", "a translation (slide)", "a glide reflection", "it got bigger"]


def one_what(r):
    s = r.choice(SH)
    kind = r.choice(["v", "h"])
    move = r.choice(WHAT[:3] * 3 + WHAT[3:])
    nx, ny = 10, 8
    for _ in range(100):
        if kind == "v":
            m = r.randint(4, 6)
            A = place(s, r.randint(0, 1), r.randint(0, 4))
            if bbox(A)[1] >= m:
                continue
            k = r.choice([2, 3]) * r.choice([1, -1])
            R_ = [reflect(p, ("v", m)) for p in A]
            B = {"a reflection": R_, "a translation (slide)": shift(A, 2 * m - bbox(A)[0] - bbox(A)[1], 0) if r.random() < 0.5 else shift(A, 5, k),
                 "a glide reflection": shift(R_, 0, k), "it got bigger": None}[move]
        else:
            m = r.randint(3, 4)
            A = place(s, r.randint(0, 5), 0)
            if bbox(A)[3] >= m:
                continue
            k = r.choice([2, 3]) * r.choice([1, -1])
            R_ = [reflect(p, ("h", m)) for p in A]
            B = {"a reflection": R_, "a translation (slide)": shift(A, k, 2 * m - bbox(A)[2] - bbox(A)[3]),
                 "a glide reflection": shift(R_, k, 0), "it got bigger": None}[move]
        if B is None:
            B = [(2 * x, 2 * y) for x, y in s]
            b = bbox(B)
            B = shift(B, nx - b[1], ny - b[3])
        if fits(A, nx, ny) and fits(B, nx, ny) and not set(A) & set(B):
            a, b = bbox(A), bbox(B)
            if a[1] < b[0] or b[1] < a[0] or a[3] < b[2] or b[3] < a[2]:
                break
    else:
        raise AssertionError
    G = Grid(nx, ny)
    G.poly(A, GREEN, "A").poly(B, BLUE, "B")
    why = {"a reflection": "B is a mirror image of A (it is flipped) and is straight across from it, the same size.",
           "a translation (slide)": "B faces the same way as A. Every corner moved the same number of squares, so it is a slide.",
           "a glide reflection": "B is flipped, so it is a reflection, but it is also slid along the mirror line. A reflection and a slide together make a glide reflection.",
           "it got bigger": "The sides of B are twice as long as the sides of A. Reflections and slides never change the size."}[move]
    return mcq_fixed(fig(G.svg("grid with shape A and shape B")) + "What happened to shape A to make shape B?", WHAT, move, why + " Answer: <b>%s</b>." % move)


CHECK = ["Yes, it is correct", "No: it is too far from the line", "No: it was slid, not flipped", "No: it is not straight across"]


def one_check(r):
    s = r.choice(SH)
    kind = r.choice(["v", "h"])
    ans = r.choice(CHECK)
    nx, ny = 10, 8
    for _ in range(100):
        if kind == "v":
            m = 5
            A = place(s, r.randint(0, 1), r.randint(0, 4))
            if bbox(A)[1] >= m:
                continue
            R_ = [reflect(p, ("v", m)) for p in A]
            B = {CHECK[0]: R_, CHECK[1]: shift(R_, 1, 0), CHECK[2]: shift(A, 2 * m - bbox(A)[0] - bbox(A)[1], 0), CHECK[3]: shift(R_, 0, r.choice([2, -2]))}[ans]
        else:
            m = 4
            A = place(s, r.randint(0, 5), 0)
            if bbox(A)[3] >= m:
                continue
            R_ = [reflect(p, ("h", m)) for p in A]
            B = {CHECK[0]: R_, CHECK[1]: shift(R_, 0, 1), CHECK[2]: shift(A, 0, 2 * m - bbox(A)[2] - bbox(A)[3]), CHECK[3]: shift(R_, r.choice([2, -2]), 0)}[ans]
        if fits(A, nx, ny) and fits(B, nx, ny) and sorted(B) != sorted(R_) or ans == CHECK[0] and fits(B, nx, ny):
            if not set(A) & set(B) or ans == CHECK[0]:
                break
    else:
        raise AssertionError
    k = Kid(r).next()
    G = Grid(nx, ny)
    G.mirror(kind, m)
    G.poly(A, GREEN, "A").poly(B, BLUE, "B")
    why = {CHECK[0]: "Every corner of B is the same distance from the line as its partner in A, on the other side, and B is flipped.",
           CHECK[1]: "B is flipped, but each corner is 1 square farther from the line than its partner in A.",
           CHECK[2]: "B faces the same way as A, so it was slid. A reflection faces the other way.",
           CHECK[3]: "B is flipped, but it has moved along the line too, so it is not straight across from A."}[ans]
    return mcq_fixed(fig(G.svg("grid with a dashed mirror line, shape A and shape B")) + "%s reflects shape A in the dashed line and draws shape B. Is shape B correct?" % k["n"], CHECK, ans, why)



def build():
    sets, R = build_sets([
        ("Reflect a point", [("collect", uniq(one_point), 20)]),
        ("Is the reflection correct?", [("collect", uniq(one_check), 20)]),
        ("Glide reflection of a point", [("collect", uniq(one_glide_pt), 20)]),
        ("Reflection, slide or glide reflection?", [("collect", uniq(one_what), 20)]),
        ("Slides on a grid", [("run", ukt.set_describe, ("rnd", ukt.People), 20)]),
    ], 70420)
    finish(sets, R)
    body = lesson('<ul><li>A <b>reflection</b> flips a figure over a line, like a mirror. Each point of the image is the same distance from the line as the original point, straight across.</li><li>The image is the same size and shape, but it faces the other way.</li><li>A <b>glide reflection</b> is a reflection and then a slide along the mirror line.</li><li>To draw an image, reflect each corner, then join the corners.</li></ul>',
        [example("P is 2 squares left of the line", ["the image is 2 squares right of the line"], "straight across, the same row")],
        [['Wrong distance from the line', 'Count the squares from the line, not from the edge.'], ['Sliding instead of flipping', 'A reflection faces the other way.'], ['Forgetting the slide', 'A glide reflection also moves along the line.']])
    faq = [('What does MATATAG Math 4 ask about reflection?', 'Draw the image of an object after applying reflection with respect to a line, including glide reflection.'), ('What is a glide reflection?', 'A reflection in a line followed by a slide along that line, like footprints in the sand.'), ('Does a reflection change the size?', 'No. Only the position and the direction it faces change.'), ('Where are glide reflections in real life?', 'Footprints, and some border patterns on cloth and walls.')]
    make('reflection-and-glide-reflection', 20, 'Measurement and Geometry', 'Grade 4: Measurement and Geometry',
         'Draw the image of an object after applying reflection with respect to a line, including glide reflection.',
         'Reflection and Glide Reflection', 'Reflection and Glide Reflection',
         'Free Grade 4 reflection worksheets for the DepEd MATATAG curriculum: reflect points and shapes in a line, glide reflections and slides on a grid. 100 questions with answers.',
         'Reflect: the same distance from the line, on the other side.', 'Glide reflection = reflect, then slide along the line.',
         body, faq, sets, seo_title=None)


if __name__ == "__main__":
    build()
