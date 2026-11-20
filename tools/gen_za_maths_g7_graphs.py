# -*- coding: utf-8 -*-
"""
South Africa Grade 7 Maths (CAPS): Graphs: Reading and Interpreting Global Graphs (Grade 7: 2.5 Graphs)
  python3 tools/gen_za_maths_g7_graphs.py
Describing trends in global graphs and taxi fare graphs (own makers), distance-time graphs (UK Year 9 makers) and
graphs of relationships (Ontario Grade 7 and BC Grade 7 makers).
Wrong answers come from real mistakes: reading the wrong axis, reading the scale wrongly, and thinking a flat line
means moving fast.
"""
import za_common
from za_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example, rand, cents, words, NBSP)
import random
import gen_uk_maths_y9_real_life_graphs as ukg
adopt(ukg)
if isinstance(getattr(ukg, 'R', None), random.Random): ukg.R = random.Random(807170)
import gen_caon_math_g7_patterns as cap
adopt(cap)
if isinstance(getattr(cap, 'R', None), random.Random): cap.R = random.Random(807171)
import gen_cabc_math_g7_linear_relations as cbl
adopt(cbl)
if isinstance(getattr(cbl, 'R', None), random.Random): cbl.R = random.Random(807172)
za_common.GRADE = "grade-7"

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


import re as _re
za_common.GBP_TO_RAND = True


def _txt(it):
    return _re.sub(r"<[^>]+>", " ", _re.sub(r"<svg.*?</svg>", " ", it["q"], flags=_re.S) + " " + " ".join(it["c"]) + " " + it["e"])


def ok7(it):
    """Grade 7: no circles, pi or standard form (they come in Grade 8 and 9)"""
    return not _re.search(r"π|\bpi\b|circumference|radius|diameter|×\s?10<sup>|standard form|scientific notation", _txt(it))


def noneg(it):
    return ok7(it) and not _re.search(r"(?<![\d)] )[−-]\d", _txt(it))


def line_svg(pts, xl, yl, xmax, ymax, xstep, ystep):
    W, H, L, B = 360, 300, 56, 250
    sx = (W - L - 20) / xmax
    sy = (B - 20) / ymax
    o = "<svg viewBox='0 0 %d %d' width='%d' height='%d' role='img' aria-label='line graph'><g font-family='Arial, Helvetica, sans-serif'>" % (W, H, W, H)
    x = 0
    while x <= xmax:
        X = L + x * sx
        o += "<line x1='%.1f' y1='20' x2='%.1f' y2='%d' stroke='#e2e2e2'/><text x='%.1f' y='%d' font-size='11' text-anchor='middle'>%d</text>" % (X, X, B, X, B + 16, x)
        x += xstep
    y = 0
    while y <= ymax:
        Y = B - y * sy
        o += "<line x1='%d' y1='%.1f' x2='%d' y2='%.1f' stroke='#e2e2e2'/><text x='%d' y='%.1f' font-size='11' text-anchor='end'>%d</text>" % (L, Y, W - 20, Y, L - 6, Y + 4, y)
        y += ystep
    o += "<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='#2b2b2b' stroke-width='2'/><line x1='%d' y1='%d' x2='%d' y2='16' stroke='#2b2b2b' stroke-width='2'/>" % (L, B, W - 16, B, L, B, L)
    o += "<polyline points='%s' fill='none' stroke='#1f5fa8' stroke-width='3'/>" % " ".join("%.1f,%.1f" % (L + a * sx, B - b * sy) for a, b in pts)
    o += "<text x='%d' y='%d' font-size='13' font-weight='700' text-anchor='middle'>%s</text>" % ((L + W - 20) // 2, B + 36, xl)
    o += "<text x='14' y='%d' font-size='13' font-weight='700' text-anchor='middle' transform='rotate(-90 14 %d)'>%s</text>" % ((B + 20) // 2, (B + 20) // 2, yl)
    return o + "</g></svg>"


STORIES = [("Water in a tank (kℓ)", "Time (hours)"), ("Height of a kite (m)", "Time (minutes)"), ("Learners in the library", "Time (hours after 08:00)"), ("Temperature (°C)", "Time (hours after 06:00)")]


def one_global(r):
    yl, xl = r.choice(STORIES)
    n = 5
    ys = [r.randint(1, 9) * 5]
    kinds = []
    for i in range(n - 1):
        k = r.choice(["up", "down", "flat"])
        kinds.append(k)
        v = ys[-1] + (r.randint(1, 4) * 5 if k == "up" else -r.randint(1, 4) * 5 if k == "down" else 0)
        if v < 0 or v > 60:
            raise AssertionError
        ys.append(v)
    if len(set(kinds)) < 3:
        raise AssertionError
    pts = [(2 * i, y) for i, y in enumerate(ys)]
    svg = fig(line_svg(pts, xl, yl, 8, 60, 1, 10))
    ivs = ["%d and %d" % (2 * i, 2 * i + 2) for i in range(n - 1)]
    q = r.choice(["flat", "down", "max", "up"])
    if q in ("flat", "down", "up"):
        idx = [i for i, k in enumerate(kinds) if k == q]
        if len(idx) != 1:
            raise AssertionError
        word = {"flat": "stay the same", "down": "decrease", "up": "increase"}[q]
        return mcq(svg + "Between which two times does the graph %s?" % word, ivs[idx[0]], [ivs[i] for i in range(n - 1) if i != idx[0]][:3],
                   "Between %s the line goes %s. <b>%s</b>." % (ivs[idx[0]], {"flat": "flat (no change)", "down": "down", "up": "up"}[q], ivs[idx[0]]))
    mx = max(ys)
    if ys.count(mx) > 1:
        raise AssertionError
    return mcq(svg + "What is the maximum value on the graph?", str(mx), [str(x) for x in sorted(set(ys) - {mx}, reverse=True)[:2]] + [str(mx + 5)],
               "The highest point of the graph is at %d. <b>%d</b>." % (mx, mx))


def one_fare(r):
    base = r.choice([10, 15, 20, 25])
    per = r.choice([5, 8, 10, 12])
    kmax = 10
    ymax = ((base + per * kmax) // 20 + 1) * 20
    svg = fig(line_svg([(0, base), (kmax, base + per * kmax)], "Distance (km)", "Fare (R)", kmax, ymax, 1, 20))
    k = r.randint(2, 9)
    what = r.choice(["fare", "start", "per"])
    if what == "fare":
        v = base + per * k
        return mcq(svg + "The graph shows the fare for a taxi trip. What is the fare for %d km?" % k, "R%d" % v, ["R%d" % x for x in (per * k, v + per, base + k)],
                   "Fare = R%d + R%d × %d = <b>R%d</b>." % (base, per, k, v))
    if what == "start":
        return mcq(svg + "The graph shows the fare for a taxi trip. What is the fare before the taxi moves?", "R%d" % base, ["R0", "R%d" % per, "R%d" % (base + per)],
                   "At 0 km the graph is at R%d. <b>R%d</b>." % (base, base))
    return mcq(svg + "The graph shows the fare for a taxi trip. By how much does the fare go up for each kilometre?", "R%d" % per, ["R%d" % base, "R%d" % (base + per), "R%d" % (per * 2)],
               "From 0 km to 1 km the fare goes from R%d to R%d: <b>R%d</b> per km." % (base, base + per, per))


def build():
    sets, R = build_sets([
        ("Increasing, decreasing and constant", [("collect", uniq(one_global), 20)]),
        ("Distance-time graphs", [("collect", ukg.one_dt, 20)]),
        ("Cost graphs", [("collect", uniq(one_fare), 20)]),
        ("Graphs of relationships", [("run", cap.set_graphs, (), 10, ok7), ("run", cbl.set_graphs, (), 10, ok7)]),
        ("Interpret the graph", [("run", ukg.problems, (), 10, ok7), ("collect", uniq(one_global), 10)]),
    ], 80717)
    finish(sets, R)
    body = lesson('<ul><li>Read the labels on both axes first.</li><li>Find what each small square is worth on the scale.</li><li>A line going up shows an increase; a line going down shows a decrease; a flat line shows no change.</li><li>On a distance-time graph, a steeper line means a higher speed.</li></ul>',
        [example("A flat part on a distance-time graph", ["distance does not change"], "the person stopped")],
        [['The wrong axis', 'Read the labels first.'], ['The scale', 'Work out each square.'], ['Flat means fast', 'Flat means not moving.']])
    faq = [('What does CAPS Grade 7 say about graphs?', 'Analyse and interpret global graphs of problem situations, describing trends such as increasing or decreasing, constant or changing, and maximum or minimum.'), ('What does a steep line mean?', 'A fast change.'), ('What is a conversion graph?', 'A graph that changes one unit into another.'), ('Can a graph go up and down?', 'Yes, it can show changes over time.')]
    make('graphs', 17, 'Patterns, Functions and Algebra', 'Grade 7: 2.5 Graphs',
         'Analyse and interpret global graphs of problem situations, with special focus on trends and features: linear or non-linear, constant, increasing or decreasing, maximum or minimum, discrete or continuous; draw global graphs from given descriptions of a problem situation.',
         'Graphs: Reading and Interpreting Global Graphs', 'Graphs',
         'Free CAPS Grade 7 graphs worksheets: conversion graphs, distance-time graphs, cost graphs and interpreting trends. 100 questions with memos.',
         'Read the axes and the scale first.', 'Flat line: no change.',
         body, faq, sets, seo_title=None)


if __name__ == "__main__":
    build()
