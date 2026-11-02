# -*- coding: utf-8 -*-
"""
CA Grade 2 Math: Measuring Length (Ontario Mathematics Curriculum 2020, Grade 2: E2.3, also E2.1, E2.2)
  python3 tools/gen_caon_math_g2_length.py
HTML attributes use single quotes (no backslashes in the JSON).
Grade 2: whole numbers to 200, very short sentences for 7-8 year olds, a picture in most questions.
Non-standard units (linking cubes and paper clips: a paper clip is exactly 2 cubes long in every picture),
centimetres and metres with benchmarks (a fingertip is about 1 cm wide, a big step is about 1 m),
reading a centimetre ruler from 0 and from other points, drawing lengths, comparing and word problems.
Every object is drawn exactly from its start mark to its end mark, and every answer is checked in code.
Wrong answers come from real mistakes: counting the marks instead of the spaces, starting at 1,
reading the end number when the object does not start at 0, counting the lines between cubes,
thinking a bigger unit gives a bigger number, mixing up cm and m, adding instead of subtracting,
and subtracting the smaller digit from the bigger one in each place.
"""
import json, os, random, re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "ca-on", "math", "grade-2")
UPDATED = "2026-11-02"
GREEN = "#006633"
RED = "#c0392b"
INK = "#2b2b2b"
GREY = "#8a8a8a"
RULER = "#f6e7a8"
FONT = "Arial, Helvetica, sans-serif"
GIRLS = ["Olivia", "Emma", "Maya", "Zoe", "Amira", "Mei", "Chloe", "Priya", "Leah", "Hana", "Ava", "Sofia"]
BOYS = ["Liam", "Noah", "Aiden", "Lucas", "Owen", "Arjun", "Ethan", "Jayden", "Benjamin", "Mateo", "Nathan", "Kai"]

PX = 24                        # one cube = one grid step; one centimetre on a ruler picture
PU = {"cube": 24, "clip": 48}  # a paper clip is exactly 2 cubes long in every picture
UNAME = {"cube": ("cube", "cubes"), "clip": ("paper clip", "paper clips"), "cm": ("cm", "cm"), "m": ("m", "m")}
CUBE_COLOURS = ["#e05a6a", "#3d7cc9"]
BAND = 24
PADL = 16
RLEN = 15


def u(n, unit):
    one, many = UNAME[unit]
    return "%d %s" % (n, one if n == 1 else many)


# ------------------------------------------------------------ helpers
def mcq(q, correct, cands, e):
    """4 choices: correct + the first 3 unique distractors (no 0 or negatives). Positions are set by balance()."""
    correct = str(correct)
    seen = {correct}
    pick = []
    for c in cands:
        c = str(c)
        if c in seen or not c or c.startswith("-") or re.match(r"^0\b", c):
            continue
        seen.add(c)
        pick.append(c)
        if len(pick) == 3:
            break
    assert len(pick) == 3, (q, correct, cands)
    return {"q": q, "c": [correct] + pick, "a": 0, "e": e}


def mcq_len(q, L, unit, cands, e):
    return mcq(q, u(L, unit), [u(c, unit) if isinstance(c, int) else c for c in cands
                               if not isinstance(c, int) or c > 0], e)


def balance(sets, rnd):
    """Spread the correct answers evenly over the 4 positions in every set (5/5/5/5)."""
    for s in sets:
        targets = [0, 1, 2, 3] * 5
        rnd.shuffle(targets)
        for it, t in zip(s["items"], targets):
            c = it["c"]
            right = c[it["a"]]
            wrong = [x for i, x in enumerate(c) if i != it["a"]]
            rnd.shuffle(wrong)
            it["c"] = wrong[:t] + [right] + wrong[t:]
            it["a"] = t


class People:
    def __init__(self, rnd):
        self.pool = [(n, "she", "her") for n in GIRLS] + [(n, "he", "his") for n in BOYS]
        rnd.shuffle(self.pool)
        self.i = 0

    def next(self):
        p = self.pool[self.i % len(self.pool)]
        self.i += 1
        return p


def cap(s):
    return s[0].upper() + s[1:]


def fig(svg):
    return "<div class='qfig'>" + svg + "</div>"


def svg_wrap(w, h, body, label, lg=True):
    return ("<svg %sxmlns='http://www.w3.org/2000/svg' viewBox='0 0 %d %d' width='%d' height='%d' "
            "role='img' aria-label='%s'><g font-family='%s'>%s</g></svg>"
            % ("data-pf='lg' " if lg else "", w, h, w, h, label, FONT, body))


def table(head, rows):
    h = "".join("<th>%s</th>" % x for x in head)
    b = "".join("<tr>" + "".join("<td>%s</td>" % c for c in r) + "</tr>" for r in rows)
    return "<div class='sn-tw'><table class='sn-table'><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>" % (h, b)


def ex(title, q, s, a):
    return ("<div class='sn-ex'><span class='sn-ex-t'>%s</span><p class='sn-ex-q'>%s</p>"
            "<p class='sn-ex-s'>%s</p><p class='sn-ex-a'>Answer: %s</p></div>" % (title, q, s, a))


def count_list(n, start=1):
    return ", ".join(str(i) for i in range(start, start + n))


def digit_slip(a, b):
    """Common mistake: subtract the smaller digit from the bigger one in each place (52 - 37 -> 25)."""
    if a < 10 or b < 10:
        return None
    t = abs(a // 10 - b // 10)
    o = abs(a % 10 - b % 10)
    r = t * 10 + o
    return r if r != a - b else None


# ------------------------------------------------------------ objects (drawn from x0 to x1 in the band yt..yb)
def draw_object(kind, x0, x1, yt, yb):
    ym = (yt + yb) / 2.0
    L = x1 - x0
    s = []
    if kind == "pencil":
        assert L >= 60
        s.append("<rect x='%.1f' y='%.1f' width='9' height='%.1f' fill='#f2a7b5' stroke='%s' stroke-width='1.2'/>" % (x0, yt + 2, yb - yt - 4, INK))
        s.append("<rect x='%.1f' y='%.1f' width='6' height='%.1f' fill='#b8b8b8' stroke='%s' stroke-width='1.2'/>" % (x0 + 9, yt + 1, yb - yt - 2, INK))
        s.append("<rect x='%.1f' y='%.1f' width='%.1f' height='%.1f' fill='#f4c430' stroke='%s' stroke-width='1.2'/>" % (x0 + 15, yt + 1, L - 33, yb - yt - 2, INK))
        s.append("<polygon points='%.1f,%.1f %.1f,%.1f %.1f,%.1f' fill='#e8c79a' stroke='%s' stroke-width='1.2' stroke-linejoin='round'/>"
                 % (x1 - 18, yt + 1, x1 - 18, yb - 1, x1, ym, INK))
        s.append("<polygon points='%.1f,%.1f %.1f,%.1f %.1f,%.1f' fill='%s'/>" % (x1 - 6, ym - 3.6, x1 - 6, ym + 3.6, x1, ym, INK))
    elif kind == "crayon":
        assert L >= 40
        s.append("<rect x='%.1f' y='%.1f' width='%.1f' height='%.1f' rx='3' fill='#3d7cc9' stroke='%s' stroke-width='1.2'/>" % (x0, yt + 2, L - 12, yb - yt - 4, INK))
        s.append("<rect x='%.1f' y='%.1f' width='%.1f' height='%.1f' fill='#9cc3ee'/>" % (x0 + 6, yt + 8, max(L - 26, 4), yb - yt - 16))
        s.append("<polygon points='%.1f,%.1f %.1f,%.1f %.1f,%.1f %.1f,%.1f' fill='#3d7cc9' stroke='%s' stroke-width='1.2' stroke-linejoin='round'/>"
                 % (x1 - 12, yt + 4, x1 - 12, yb - 4, x1, ym + 2.5, x1, ym - 2.5, INK))
    elif kind == "leaf":
        xm = (x0 + x1) / 2
        s.append("<path d='M%.1f %.1f Q%.1f %.1f %.1f %.1f Q%.1f %.1f %.1f %.1f Z' fill='#9cc49a' stroke='%s' stroke-width='1.4'/>"
                 % (x0, ym, xm, yt - 4, x1, ym, xm, yb + 4, x0, ym, GREEN))
        s.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='1.2'/>" % (x0 + 2, ym, x1 - 3, ym, GREEN))
    elif kind == "ribbon":
        s.append("<rect x='%.1f' y='%.1f' width='%.1f' height='%.1f' fill='#e05a6a' stroke='%s' stroke-width='1.2'/>" % (x0, yt + 6, L, yb - yt - 12, INK))
    elif kind == "strip of paper":
        s.append("<rect x='%.1f' y='%.1f' width='%.1f' height='%.1f' fill='#cfe3f7' stroke='%s' stroke-width='1.2'/>" % (x0, yt + 4, L, yb - yt - 8, INK))
    elif kind == "craft stick":
        s.append("<rect x='%.1f' y='%.1f' width='%.1f' height='%.1f' rx='8' fill='#e6c88f' stroke='%s' stroke-width='1.2'/>" % (x0, yt + 4, L, yb - yt - 8, INK))
    elif kind == "eraser":
        s.append("<rect x='%.1f' y='%.1f' width='%.1f' height='%.1f' rx='3' fill='#f2a7b5' stroke='%s' stroke-width='1.2'/>" % (x0, yt + 2, L, yb - yt - 4, INK))
        s.append("<rect x='%.1f' y='%.1f' width='%.1f' height='%.1f' fill='#5dade2' stroke='%s' stroke-width='1.2'/>" % (x0 + L * 0.45, yt + 2, L * 0.4, yb - yt - 4, INK))
    elif kind in ("caterpillar", "worm"):
        k = max(3, int(round(L / 15.0)))
        d = L / k
        body, head, line = (("#8cc63f", "#4e9a3f", GREEN) if kind == "caterpillar" else ("#f4a6a0", "#e07b73", "#a34d47"))
        for i in range(k):
            col = head if i == k - 1 else body
            s.append("<circle cx='%.1f' cy='%.1f' r='%.1f' fill='%s' stroke='%s' stroke-width='1.1'/>"
                     % (x0 + d * (i + 0.5), ym + 2, min(d / 2 - 0.4, 10), col, line))
        s.append("<circle cx='%.1f' cy='%.1f' r='1.6' fill='%s'/>" % (x1 - d * 0.35, ym, INK))
    elif kind == "marker":
        cw = min(0.3 * L, 45)
        s.append("<rect x='%.1f' y='%.1f' width='%.1f' height='%.1f' rx='3' fill='#f4f4f4' stroke='%s' stroke-width='1.2'/>" % (x0, yt + 3, L - cw, yb - yt - 6, INK))
        s.append("<rect x='%.1f' y='%.1f' width='%.1f' height='%.1f' rx='4' fill='#2e8b57' stroke='%s' stroke-width='1.2'/>" % (x1 - cw, yt + 1, cw, yb - yt - 2, INK))
    elif kind == "straw":
        s.append("<rect x='%.1f' y='%.1f' width='%.1f' height='%.1f' fill='#ffffff' stroke='%s' stroke-width='1.2'/>" % (x0, yt + 7, L, yb - yt - 14, INK))
        x = x0 + 6
        while x + 6 < x1:
            s.append("<rect x='%.1f' y='%.1f' width='6' height='%.1f' fill='#e05a6a'/>" % (x, yt + 7.6, yb - yt - 15.2))
            x += 14
    elif kind == "paper clip":
        s.append("<rect x='%.1f' y='%.1f' width='%.1f' height='%.1f' rx='%.1f' fill='none' stroke='#6d7a86' stroke-width='2.4'/>"
                 % (x0 + 1.2, yt + 4, L - 2.4, yb - yt - 8, (yb - yt - 8) / 2.0))
        s.append("<rect x='%.1f' y='%.1f' width='%.1f' height='%.1f' rx='%.1f' fill='none' stroke='#6d7a86' stroke-width='2.4'/>"
                 % (x0 + 7, yt + 8.5, L - 18, yb - yt - 17, (yb - yt - 17) / 2.0))
    elif kind == "key":
        assert L >= 60
        r = (yb - yt) / 2.0 - 1
        s.append("<rect x='%.1f' y='%.1f' width='%.1f' height='6' fill='#e3b94a' stroke='%s' stroke-width='1.2'/>" % (x0 + 2 * r - 2, ym - 3, L - 2 * r + 2, INK))
        for t in range(3):
            s.append("<rect x='%.1f' y='%.1f' width='5' height='%d' fill='#e3b94a' stroke='%s' stroke-width='1.1'/>"
                     % (x1 - 6 - t * 9, ym + 3, 6 - 2 * (t % 2), INK))
        s.append("<circle cx='%.1f' cy='%.1f' r='%.1f' fill='#e3b94a' stroke='%s' stroke-width='1.2'/>" % (x0 + r, ym, r, INK))
        s.append("<circle cx='%.1f' cy='%.1f' r='3' fill='#fff' stroke='%s' stroke-width='1'/>" % (x0 + r * 0.7, ym, INK))
    elif kind == "line":
        s.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='4' stroke-linecap='butt'/>" % (x0, ym, x1, ym, RED))
        s.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='2'/>" % (x0, ym - 7, x0, ym + 7, RED))
        s.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='2'/>" % (x1, ym - 7, x1, ym + 7, RED))
    else:
        raise ValueError(kind)
    return "".join(s)


def guide(x, y0, y1):
    return ("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='1' stroke-dasharray='3 2'/>"
            % (x, y0, x, y1, GREY))


# ------------------------------------------------------------ non-standard units
def cube(x, y, i):
    col = CUBE_COLOURS[i % 2]
    return ("<rect x='%.1f' y='%.1f' width='%d' height='%d' fill='%s' stroke='%s' stroke-width='1.2'/>"
            "<rect x='%.1f' y='%.1f' width='%d' height='%d' fill='none' stroke='#ffffff' stroke-opacity='0.6' stroke-width='1'/>"
            % (x, y, PU["cube"], BAND, col, INK, x + 6, y + 6, PU["cube"] - 12, BAND - 12))


def unit_row(x0, y, n, unit, mode="exact"):
    """n units laid from x0. mode: exact (end to end), gap (spaces between), overlap."""
    pu = PU[unit]
    assert not (mode == "overlap" and unit == "cube"), "overlap pictures use paper clips"
    step = {"exact": pu, "gap": pu + 8, "overlap": pu - 12}[mode]
    s = []
    for i in range(n):
        x = x0 + i * step
        if unit == "cube":
            s.append(cube(x, y, i))
        else:
            s.append(draw_object("paper clip", x, x + pu, y, y + BAND))
    return "".join(s), x0 + (n - 1) * step + pu


def measure_block(kind, L, unit, y, n=None, mode="exact"):
    x0 = PADL
    x1 = x0 + L * PU[unit]
    n = n if n is not None else L
    s = [guide(x0, y - 3, y + 2 * BAND + 8), guide(x1, y - 3, y + 2 * BAND + 8),
         draw_object(kind, x0, x1, y, y + BAND)]
    row, rr = unit_row(x0, y + BAND + 6, n, unit, mode)
    s.append(row)
    return "".join(s), max(x1, rr), y + 2 * BAND + 8


def measure_svg(kind, L, unit, total=None):
    body, right, bottom = measure_block(kind, L, unit, 6, total)
    lab = "%s %d %s long, above %d %s laid end to end" % (kind, L, UNAME[unit][1], total or L, UNAME[unit][1])
    return svg_wrap(int(right + PADL), int(bottom + 4), body, lab)


def n_gap(L, unit):
    pu = PU[unit]
    return (L * pu + 8) // (pu + 8)


def n_over(L, unit):
    pu = PU[unit]
    assert ((L - 1) * pu) % (pu - 12) == 0, L
    return (L - 1) * pu // (pu - 12) + 1


def wrong_svg(kind, L, unit, mode):
    if mode == "gap":
        body, right, bottom = measure_block(kind, L, unit, 6, n=n_gap(L, unit), mode="gap")
    else:
        body, right, bottom = measure_block(kind, L, unit, 6, n=n_over(L, unit), mode="overlap")
    return svg_wrap(int(right + PADL), int(bottom + 4), body, "%s measured with %s: %s" % (kind, UNAME[unit][1], mode))


def two_units_svg(kind, cubes):
    assert cubes % 2 == 0
    x0, x1 = PADL, PADL + cubes * PU["cube"]
    s = [guide(x0, 3, 6 + 3 * BAND + 18), guide(x1, 3, 6 + 3 * BAND + 18), draw_object(kind, x0, x1, 6, 6 + BAND)]
    r1, e1 = unit_row(x0, 6 + BAND + 6, cubes, "cube")
    r2, e2 = unit_row(x0, 6 + 2 * BAND + 12, cubes // 2, "clip")
    assert e1 == x1 and e2 == x1
    s += [r1, r2]
    return svg_wrap(int(x1 + PADL), int(6 + 3 * BAND + 20), "".join(s),
                    "%s measured with %d cubes and with %d paper clips" % (kind, cubes, cubes // 2))


def about_svg(kind, cubes):
    """An object an odd number of cubes long, measured with paper clips: the last clip sticks out past the end."""
    assert cubes % 2 == 1
    n = cubes // 2 + 1
    x0, x1 = PADL, PADL + cubes * PX
    y = 6
    s = [guide(x0, y - 3, y + 2 * BAND + 8), guide(x1, y - 3, y + 2 * BAND + 8), draw_object(kind, x0, x1, y, y + BAND)]
    row, rr = unit_row(x0, y + BAND + 6, n, "clip")
    s.append(row)
    assert rr == x1 + PX
    return svg_wrap(int(rr + PADL), y + 2 * BAND + 12, "".join(s),
                    "%s between %d and %d paper clips long" % (kind, n - 1, n))


# ------------------------------------------------------------ centimetre ruler
def ruler_body(y):
    """Ruler 0..15 cm with whole-centimetre marks. Top edge at y (height 42)."""
    X = lambda k: PADL + PX * k
    right = X(RLEN) + 16 + 20 + 8
    s = ["<rect x='%.1f' y='%.1f' width='%.1f' height='42' rx='3' fill='%s' stroke='%s' stroke-width='1.5'/>"
         % (PADL - 10, y, right - (PADL - 10), RULER, INK)]
    for k in range(RLEN + 1):
        s.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='2'/>" % (X(k), y, X(k), y + 18, INK))
        s.append("<text x='%.1f' y='%.1f' font-size='15' font-weight='700' fill='%s' text-anchor='middle'>%d</text>" % (X(k), y + 36, INK, k))
    s.append("<text x='%.1f' y='%.1f' font-size='14' fill='%s'>cm</text>" % (X(RLEN) + 16, y + 36, INK))
    return "".join(s), right + 6


def ruler_svg(objs):
    """objs: list of (kind, start, end). Each object gets its own band above the ruler."""
    X = lambda k: PADL + PX * k
    band, gap = 24, 8
    top = 6
    rtop = top + len(objs) * (band + gap)
    s = []
    for i, (kind, a, b) in enumerate(objs):
        assert 0 <= a < b <= RLEN, (kind, a, b)
        yt = top + i * (band + gap)
        s.append(guide(X(a), yt - 3, rtop))
        s.append(guide(X(b), yt - 3, rtop))
        s.append(draw_object(kind, X(a), X(b), yt, yt + band))
    body, W = ruler_body(rtop)
    desc = " and ".join("%s from %d to %d" % (k, a, b) for k, a, b in objs)
    return svg_wrap(int(W), int(rtop + 48), "".join(s) + body, "%s above a ruler in centimetres" % desc)


# ============================================================ set 1: non-standard units
S1 = [("crayon", 5, "cube", None), ("key", 3, "cube", None), ("eraser", 2, "clip", None), ("pencil", 8, "cube", None),
      ("straw", 3, "clip", None), ("caterpillar", 7, "cube", None), ("marker", 4, "clip", None),
      ("ribbon", 10, "cube", None), ("craft stick", 6, "cube", 9)]


def set_units(P):
    its = []
    asks = ["How many %s long is the %s?", "Count the %s. How long is the %s?"]
    for i, (kind, L, unit, total) in enumerate(S1):
        un = UNAME[unit][1]
        if total:
            q = "Count only the %s under the %s. How long is the %s?" % (un, kind, kind)
        else:
            q = asks[i % 2] % (un, kind)
        q = fig(measure_svg(kind, L, unit, total)) + q
        e = "Count the %s from one end of the %s to the other: %s. It is <b>%s</b> long." % (un, kind, count_list(L), u(L, unit))
        if total:
            e += " There are %d %s in the row, but only %d are under the %s. Do not count the extra ones." % (total, un, L, kind)
            cands = [total, L + 1, L - 1]
        else:
            e += " Count the %s, not the lines between them." % un
            cands = [L - 1, L + 1, L + 2]
        its.append(mcq_len(q, L, unit, cands, e))

    q = fig(wrong_svg("crayon", 4, "clip", "gap")) + "Is this a good way to measure the crayon?"
    its.append(mcq(q, "No, there are gaps.", ["Yes, it is right.", "No, they overlap.", "No, the clips are too small."],
                   "<b>No, there are gaps</b> between the paper clips. The gaps are not counted, so the number is too small. "
                   "Push the paper clips together so they touch."))
    q = fig(wrong_svg("ribbon", 7, "clip", "overlap")) + "Is this a good way to measure the ribbon?"
    its.append(mcq(q, "No, they overlap.", ["Yes, it is right.", "No, there are gaps.", "No, the clips are too small."],
                   "<b>No, the paper clips overlap.</b> Some lie on top of others, so you count too many. Lay them end to end."))

    for kind, cubes in [("pencil", 8), ("ribbon", 10)]:
        clips = cubes // 2
        q = fig(two_units_svg(kind, cubes)) + "The %s is %d cubes long. How many paper clips long is it?" % (kind, cubes)
        e = ("Look at the bottom row. Count the paper clips: %s. It is <b>%s</b> long. "
             "A paper clip is longer than a cube, so you need fewer of them." % (count_list(clips), u(clips, "clip")))
        its.append(mcq_len(q, clips, "clip", [cubes, cubes * 2, clips + 1], e))
    its.append(mcq("A pencil is 10 cubes long. It is 5 paper clips long. Why are there more cubes?",
                   "A cube is shorter.", ["A cube is longer.", "The pencil grew.", "Someone made a mistake."],
                   "A cube is shorter than a paper clip. It takes <b>more cubes</b> to cover the same pencil. "
                   "Smaller unit, bigger number."))
    its.append(mcq("You measure a desk with cubes. Then you use paper clips. Which number is bigger?", "the cubes",
                   ["the paper clips", "They are the same.", "You cannot tell."],
                   "A cube is shorter than a paper clip. You need more short units to cover the desk. "
                   "So <b>the cubes</b> give the bigger number."))
    its.append(mcq("You measure the same table with each unit. Which unit gives the biggest number?", "linking cubes",
                   ["paper clips", "pencils", "hockey sticks"],
                   "The smallest unit gives the biggest number. <b>Linking cubes</b> are the smallest here, "
                   "so you need the most of them."))
    q = fig(about_svg("pencil", 7)) + "The paper clips do not fit exactly. How long is the pencil?"
    its.append(mcq(q, "between 3 and 4 clips", ["3 paper clips", "4 paper clips", "7 paper clips"],
                   "3 paper clips are not long enough. 4 paper clips go past the end. So the pencil is "
                   "<b>between 3 and 4 paper clips</b> long. Use smaller units, like cubes, to be exact."))
    a, b = P.next(), P.next()
    its.append(mcq("%s and %s measure the same mat with their hands. %s gets 8 hands. %s gets 10 hands. Why?"
                   % (a[0], b[0], a[0], b[0]), "Their hands are not the same size.",
                   ["The mat changed.", "%s counted wrong." % a[0], "Hands are always 10."],
                   "%s has bigger hands, so fewer hands fit. Units of <b>different sizes</b> give different numbers. "
                   "That is why we use units that are all the same, like cubes or centimetres." % a[0]))
    nm, he, his = P.next()
    its.append(mcq_len("A paper clip is as long as 2 cubes. %s’s book is 12 cubes long. How many paper clips long is it?" % nm,
                       6, "clip", [12, 24, 10],
                       "Each paper clip covers 2 cubes. Count by 2s to 12: 2, 4, 6, 8, 10, 12. That is 6 jumps. "
                       "The book is <b>6 paper clips</b> long."))
    nm, he, his = P.next()
    its.append(mcq("%s’s scarf is 6 big steps long. %s ribbon is 6 paper clips long. Which is longer?" % (nm, cap(his)),
                   "the scarf", ["the ribbon", "They are the same.", "You cannot tell."],
                   "Both numbers are 6, but the units are different. A big step is much longer than a paper clip. "
                   "So <b>the scarf</b> is longer. Always look at the unit."))
    order = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19]
    its = [its[i] for i in order]
    assert len(its) == 20, len(its)
    return {"title": "Measure with cubes and paper clips", "items": its}


# ============================================================ set 2: centimetres or metres
EST = [  # (question, answer, wrong, explanation)
    ("About how long is a ladybug?", "1 cm", ["1 m", "10 cm", "10 m"],
     "A ladybug is about as wide as your fingertip. That is about <b>1 cm</b>."),
    ("About how long is a paper clip?", "3 cm", ["3 m", "30 cm", "1 m"],
     "A paper clip is about 3 fingertips long, so it is about <b>3 cm</b>. 3 m is about 3 big steps."),
    ("About how long is a crayon?", "9 cm", ["9 m", "90 cm", "1 cm"],
     "A crayon fits in your hand. That is about <b>9 cm</b>. 9 m is about as long as a classroom."),
    ("About how long is a new pencil?", "18 cm", ["18 m", "180 cm", "2 cm"],
     "A new pencil is a bit longer than your hand. That is about <b>18 cm</b>. 18 m is longer than a school bus."),
    ("About how wide is a classroom door?", "1 m", ["1 cm", "10 m", "10 cm"],
     "A door is about as wide as one big step. That is about <b>1 m</b>."),
    ("About how tall is a door?", "2 m", ["2 cm", "20 m", "20 cm"],
     "A door is taller than a grown-up. It is about 2 metre sticks tall: <b>2 m</b>."),
    ("About how tall is a Grade 2 student?", "120 cm", ["120 m", "12 cm", "20 cm"],
     "A Grade 2 student is a bit taller than a metre stick. 1 m is 100 cm, so about <b>120 cm</b> makes sense."),
    ("About how long is a canoe?", "5 m", ["5 cm", "50 m", "50 cm"],
     "A canoe is about 5 big steps long. That is about <b>5 m</b>. 5 cm is shorter than your finger."),
    ("About how long is a school bus?", "12 m", ["12 cm", "1 m", "120 m"],
     "A school bus is about 12 big steps long: <b>12 m</b>. 1 m is only as wide as a door."),
    ("About how long is the school gym?", "30 m", ["30 cm", "3 m", "300 m"],
     "A gym is about 30 big steps long. That is about <b>30 m</b>. 30 cm is about as long as a ruler."),
]


def set_cm_m(P):
    its = []
    its.append(mcq("Which is longer, 1 cm or 1 m?", "1 m", ["1 cm", "They are the same.", "You cannot tell."],
                   "<b>1 m</b> is much longer. A metre is about one big step. A centimetre is about as wide as your fingertip."))
    its.append(mcq("What is about 1 cm wide?", "your fingertip", ["one big step", "a door", "your desk"],
                   "The tip of your finger is about <b>1 cm</b> wide. Use it to picture a centimetre."))
    its.append(mcq("What is about 1 m long?", "one big step", ["your fingertip", "a crayon", "a school bus"],
                   "One big step is about <b>1 m</b>. A metre stick is 1 m long."))
    its.append(mcq_len("How many centimetres make 1 metre?", 100, "cm", [10, 1000, 50],
                       "A metre stick has 100 small spaces. Each one is 1 cm. So <b>100 cm = 1 m</b>."))
    for q, a, w, e in EST[:5]:
        its.append(mcq(q, a, w, e))
    its.append(mcq("Which would you measure in metres?", "the length of the hallway",
                   ["a crayon", "a paper clip", "an eraser"],
                   "Metres are for long things. <b>The hallway</b> is long. A crayon, a paper clip and an eraser are small, "
                   "so use centimetres for them."))
    its.append(mcq("Which would you measure in centimetres?", "a mitten",
                   ["the soccer field", "the school yard", "the skating rink"],
                   "Centimetres are for small things. <b>A mitten</b> is small. The field, the yard and the rink are long, "
                   "so use metres for them."))
    its.append(mcq("Which tool is best to measure the classroom?", "a metre stick",
                   ["a 15 cm ruler", "linking cubes", "a paper clip"],
                   "The classroom is long. <b>A metre stick</b> is 1 m long, so you need only a few. "
                   "A short ruler, cubes or a paper clip would take a very long time."))
    for q, a, w, e in EST[5:]:
        its.append(mcq(q, a, w, e))
    its.append(mcq_len("A table is 2 m long. How many centimetres long is it?", 200, "cm", [2, 20, 102],
                       "1 m is 100 cm. 2 m is 100 + 100 = <b>200 cm</b>. The number of centimetres is bigger "
                       "because a centimetre is shorter."))
    its.append(mcq("Which is longer, 1 m or 90 cm?", "1 m", ["90 cm", "They are the same.", "You cannot tell."],
                   "1 m is 100 cm. 100 cm is more than 90 cm, so <b>1 m</b> is longer. Do not just look at the bigger number."))
    nm, he, his = P.next()
    m = P.next()
    its.append(mcq("%s’s rope is 1 m long. %s’s rope is 120 cm long. Whose rope is longer?" % (nm, m[0]),
                   "%s’s rope" % m[0], ["%s’s rope" % nm, "They are the same.", "You cannot tell."],
                   "1 m is 100 cm. 120 cm is more than 100 cm, so <b>%s’s rope</b> is longer." % m[0]))
    assert len(its) == 20, len(its)
    return {"title": "Centimetres or metres?", "items": its}


# ============================================================ set 3: read a ruler from 0
S3 = [("eraser", 3), ("key", 4), ("paper clip", 3), ("crayon", 5), ("leaf", 6), ("caterpillar", 7), ("worm", 8),
      ("crayon", 9), ("straw", 10), ("marker", 11), ("craft stick", 12), ("pencil", 13), ("strip of paper", 14),
      ("ribbon", 15)]


def zero_e(obj, L):
    e = "The %s starts at 0 and ends at %d. " % (obj, L)
    if L <= 8:
        e += "Count the spaces: %s. " % count_list(L)
    e += "It is <b>%d cm</b> long. Do not count the marks: there are %d marks, because the 0 mark is not a space." % (L, L + 1)
    return e


def set_from_zero(P):
    its = []
    its.append(mcq("You measure with a ruler. Where do you put one end of the object?", "at the 0 mark",
                   ["at the 1 mark", "at the edge of the ruler", "anywhere"],
                   "Put the end at <b>0</b>. Some rulers have a little space before the 0, so do not use the edge. "
                   "If you start at 1, the number at the end is 1 too big."))
    asks = ["How long is the %s?", "How many centimetres long is the %s?", "Measure the %s. How long is it?"]
    for i, (obj, L) in enumerate(S3):
        q = fig(ruler_svg([(obj, 0, L)])) + asks[i % 3] % obj
        its.append(mcq_len(q, L, "cm", [L + 1, L - 1, u(L, "m"), L + 2], zero_e(obj, L)))
        if i == 6:
            its.append(mcq("What do you count to find a length on a ruler?", "the spaces",
                           ["the marks", "all the numbers", "the last number on the ruler"],
                           "Each space from one mark to the next is 1 cm. Count the <b>spaces</b>, not the marks. "
                           "A 3 cm eraser covers 3 spaces but touches 4 marks."))
    nm, he, his = P.next()
    q = fig(ruler_svg([("line", 0, 7)])) + "%s drew this red line. How long is it?" % nm
    its.append(mcq_len(q, 7, "cm", [8, 6, 14],
                       "The line starts at 0 and ends at 7. It covers 7 spaces, so it is <b>7 cm</b> long. "
                       "There are 8 marks, but count the spaces."))
    q = fig(ruler_svg([("line", 0, 5)])) + "Owen wants to draw a line 8 cm long. He drew this much. How many more centimetres must he draw?"
    its.append(mcq_len(q, 3, "cm", [8, 5, 13, 4],
                       "The line ends at 5. Owen needs to get to 8. Count on from 5: 6, 7, 8. That is 3 spaces. "
                       "8 − 5 = 3, so he must draw <b>3 cm</b> more."))
    nm, he, his = P.next()
    its.append(mcq("%s draws a line 6 cm long. %s starts at 0. Where should %s stop?" % (nm, cap(he), he), "at 6",
                   ["at 7", "at 5", "at 12"],
                   "Start at 0 and draw to <b>6</b>. That covers 6 spaces, so the line is 6 cm long. "
                   "If you stop at 7, the line is 7 cm long."))
    nm, he, his = P.next()
    its.append(mcq_len("%s measures a straw. It covers 12 spaces on the ruler and touches 13 marks. How long is the straw?" % nm,
                       12, "cm", [13, 11, 25],
                       "Each space is 1 cm. Count the spaces, not the marks: 12 spaces is <b>12 cm</b>. "
                       "There is always one more mark than spaces."))
    assert len(its) == 20, len(its)
    return {"title": "Read a ruler that starts at 0", "items": its}


# ============================================================ set 4: not starting at 0
S4 = [("eraser", 1, 4), ("crayon", 2, 7), ("key", 3, 6), ("leaf", 1, 8), ("caterpillar", 4, 9), ("paper clip", 5, 8),
      ("marker", 2, 10), ("worm", 6, 13), ("straw", 3, 12), ("pencil", 1, 11), ("craft stick", 5, 14), ("ribbon", 4, 15)]


def not_zero_e(obj, a, b):
    L = b - a
    e = "The %s starts at %d, not at 0. " % (obj, a)
    if L <= 6:
        e += "Count on from %d: %s. That is %d spaces. Or subtract: " % (a, count_list(L, a + 1), L)
    else:
        e += "Subtract: "
    e += "%d − %d = %d. So it is <b>%d cm</b> long. %d is where it ends, not how long it is." % (b, a, L, L, b)
    return e


def set_not_zero(P):
    its = []
    for i, (obj, a, b) in enumerate(S4):
        L = b - a
        q = fig(ruler_svg([(obj, a, b)])) + ("How long is the %s?" if i % 2 == 0 else
                                             "The %s does not start at 0. How many centimetres long is it?") % obj
        its.append(mcq_len(q, L, "cm", [b, L + 1, a, L - 1, a + b], not_zero_e(obj, a, b)))

    nm, he, his = P.next()
    its.append(mcq_len("The end of %s’s ruler broke off, so it starts at 4. %s puts a paper clip at the 4. "
                       "The paper clip ends at 7. How long is it?" % (nm, cap(he)), 3, "cm", [7, 4, 11],
                       "Count from 4, not from 0: 5, 6, 7 is 3 spaces. 7 − 4 = 3, so the paper clip is <b>3 cm</b> long."))
    nm, he, his = P.next()
    its.append(mcq_len("%s’s ruler starts at 3 because the end is broken. A marker starts at 3 and ends at 11. "
                       "How long is the marker?" % nm, 8, "cm", [11, 9, 14],
                       "Subtract the start from the end: 11 − 3 = 8. The marker is <b>8 cm</b> long."))
    nm, he, his = P.next()
    its.append(mcq("%s puts the end of a crayon at 1, not at 0. The other end is at 9. %s says the crayon is 9 cm. "
                   "What did %s do wrong?" % (nm, cap(he), he), "%s read the end number." % cap(he),
                   ["%s counted the spaces." % cap(he), "%s added 1 and 9." % cap(he), "%s used metres." % cap(he)],
                   "The crayon starts at 1, so 9 is too big. Count from 1 to 9: 9 − 1 = 8. The crayon is 8 cm long."))
    nm, he, his = P.next()
    its.append(mcq_len("A pencil starts at 3 and ends at 12 on a ruler. %s counts the marks from 3 to 12 and gets 10. "
                       "How long is the pencil?" % nm, 9, "cm", [10, 12, 15],
                       "Count spaces, not marks. From 3 to 12 there are 10 marks but only 9 spaces. 12 − 3 = 9, "
                       "so the pencil is <b>9 cm</b> long."))
    nm, he, his = P.next()
    its.append(mcq_len("%s measures a key on a ruler. One end is at 5. The other end is at 9. How long is the key?" % nm,
                       4, "cm", [9, 5, 14, 3],
                       "The key starts at 5, not at 0. Count the spaces from 5 to 9: 6, 7, 8, 9. That is 4. "
                       "Or subtract: 9 − 5 = 4. The key is <b>4 cm</b> long."))
    q = fig(ruler_svg([("crayon", 0, 5), ("key", 3, 8)])) + "Look at the crayon and the key. Which is true?"
    its.append(mcq(q, "They are the same length.", ["The key is longer.", "The crayon is longer.", "You cannot tell."],
                   "The crayon goes from 0 to 5: 5 cm. The key goes from 3 to 8: 8 − 3 = 5 cm. "
                   "<b>They are the same length.</b> The key ends at a bigger number, but it also starts later."))
    nm, he, his = P.next()
    its.append(mcq("%s starts a line at 4. %s draws it 6 cm long. Where does the line end?" % (nm, cap(he)), "at 10",
                   ["at 6", "at 9", "at 11"],
                   "Start at 4 and count 6 spaces: 5, 6, 7, 8, 9, 10. Or add: 4 + 6 = 10. The line ends <b>at 10</b>."))
    nm, he, his = P.next()
    its.append(mcq("%s starts a line at 2. %s wants it to be 7 cm long. Where should %s stop?" % (nm, cap(he), he), "at 9",
                   ["at 7", "at 8", "at 5"],
                   "Start at 2 and count 7 spaces: 3, 4, 5, 6, 7, 8, 9. Or add: 2 + 7 = 9. Stop <b>at 9</b>. "
                   "If you stop at 7, the line is only 5 cm long."))
    order = [0, 1, 2, 3, 12, 4, 5, 6, 13, 7, 8, 14, 9, 15, 10, 16, 11, 17, 18, 19]
    assert sorted(order) == list(range(20))
    its = [its[i] for i in order]
    assert len(its) == 20, len(its)
    return {"title": "When the object does not start at 0", "items": its}


# ============================================================ set 5: compare and word problems
S5 = [("pencil", 12, "crayon", 7), ("straw", 10, "eraser", 3), ("ribbon", 15, "key", 6), ("marker", 11, "caterpillar", 5)]


def diff_e(a, b, d, unit):
    e = "Subtract the shorter length from the longer one: %d − %d = <b>%d %s</b>. " % (a, b, d, unit)
    if 2 <= d <= 6:
        e += "Or count on from %d to %d: %s. " % (b, a, count_list(d, b + 1))
    elif a >= 20:
        e += "Check by adding: %d + %d = %d. " % (b, d, a)
    e += "Do not add: %d + %d = %d is the total, not the difference." % (a, b, a + b)
    return e


def set_problems(P):
    its = []
    for A, a, B, b in S5:
        d = a - b
        q = fig(ruler_svg([(A, 0, a), (B, 0, b)])) + "How much longer is the %s than the %s?" % (A, B)
        e = ("Both start at 0. The %s ends at %d and the %s ends at %d. %d − %d = %d. The %s is <b>%d cm</b> longer."
             % (A, a, B, b, a, b, d, A, d))
        its.append(mcq_len(q, d, "cm", [a, a + b, d + 1, d - 1], e))
    q = fig(ruler_svg([("straw", 0, 7), ("pencil", 5, 11)])) + "Which is longer?"
    its.append(mcq(q, "the straw", ["the pencil", "They are the same.", "You cannot tell."],
                   "The straw goes from 0 to 7: 7 cm. The pencil goes from 5 to 11: 11 − 5 = 6 cm. "
                   "<b>The straw</b> is longer, even though the pencil ends at a bigger number."))
    its.append(mcq("Which length is the longest?", "1 m", ["90 cm", "60 cm", "45 cm"],
                   "1 m is 100 cm. 100 cm is more than 90, 60 or 45 cm, so <b>1 m</b> is the longest."))

    # word problems: (template, answer, wrong, explanation)
    W = []

    def sub(tpl, a, b, unit, extra=None):
        d = a - b
        cands = [digit_slip(a, b), a + b, d + 1, d - 1, a]
        if extra:
            cands = extra + cands
        W.append((tpl, d, unit, [c for c in cands if c is not None], diff_e(a, b, d, unit)))

    def add(tpl, a, b, unit, e):
        t = a + b
        noreg = t - 10 if (a % 10 + b % 10) >= 10 else None
        cands = [noreg, a - b if a > b else b - a, t + 1, t - 1]
        W.append((tpl, t, unit, [c for c in cands if c is not None and c > 0], e))

    sub("{N} found two worms. One is 12 cm long. The other is 7 cm long. How much longer is the long worm?", 12, 7, "cm")
    sub("{N}’s paper airplane flew 9 m. {M}’s flew 6 m. How much farther did {N}’s airplane fly?", 9, 6, "m")
    sub("{N}’s pencil was 17 cm long. After a month of school, it is 9 cm long. How much shorter is it now?", 17, 9, "cm")
    sub("Two icicles hang from the roof. One is 34 cm long. The other is 18 cm long. How much longer is the long icicle?", 34, 18, "cm")
    sub("{N} found a Canada goose feather 26 cm long and a robin feather 9 cm long. How much longer is the goose feather?", 26, 9, "cm")
    sub("A bean plant was 14 cm tall. Now it is 31 cm tall. How many centimetres did it grow?", 31, 14, "cm")
    sub("{N} has a ribbon 50 cm long. {He} cuts off 18 cm for a card. How much ribbon is left?", 50, 18, "cm")
    sub("In gym class, {N} jumped 96 cm. {M} jumped 88 cm. How much farther did {N} jump?", 96, 88, "cm")
    sub("A sunflower is 92 cm tall. A tomato plant is 58 cm tall. How much taller is the sunflower?", 92, 58, "cm")
    sub("The Terry Fox Run path at school is 100 m long. {N} has run 65 m. How many more metres must {he} run?", 100, 65, "m")
    W.append(("{N}’s snow fort wall is 70 cm tall. {He} wants it to be 1 m tall. How many more centimetres must {he} build?",
              30, "cm", [70, 170, 31, 29],
              "1 m is 100 cm. 100 − 70 = <b>30 cm</b>. Count on by 10s from 70: 80, 90, 100. That is 3 tens, or 30."))
    add("{N} makes a paper chain for Canada Day. One part is 45 cm long. Another part is 38 cm long. "
        "{He} joins them. How long is the chain now?", 45, 38, "cm",
        "Joining makes it longer, so add: 45 + 38 = <b>83 cm</b>. 5 + 8 = 13, so regroup 10 ones as 1 ten.")
    add("A snowman is 85 cm tall. {N} puts a hat on top that is 12 cm tall. How tall is the snowman now?", 85, 12, "cm",
        "The hat makes the snowman taller, so add: 85 + 12 = <b>97 cm</b>.")
    add("The skating rink at the park is 45 m long. {N} skates to the end and back. How far does {he} skate?", 45, 45, "m",
        "To the end is 45 m. Back is 45 m more. 45 + 45 = <b>90 m</b>.")
    for tpl, ans, unit, cands, e in W:
        nm, he, his = P.next()
        m = P.next()[0] if "{M}" in tpl else ""
        q = tpl.format(N=nm, M=m, he=he, He=cap(he), his=his)
        e = e.replace("{N}", nm)
        its.append(mcq_len(q, ans, unit, cands, e))
    assert len(its) == 20, len(its)
    return {"title": "Compare lengths and word problems", "items": its}


# ============================================================ lesson
def body_html():
    return (
        "<h2>Measure with units that are all the same</h2>"
        "<p>Lay units <b>end to end</b> along the object. Start right at one end and stop at the other end. "
        "No gaps and no overlaps. Then count the units.</p>"
        "<figure class='sn-fig'>" + measure_svg("crayon", 6, "cube") +
        "<figcaption>6 cubes fit from one end of the crayon to the other. The crayon is 6 cubes long.</figcaption></figure>"
        "<p>A paper clip is as long as 2 cubes. The same crayon is 6 cubes or 3 paper clips. "
        "A <b>smaller unit gives a bigger number</b>.</p>"
        "<figure class='sn-fig'>" + two_units_svg("crayon", 6) +
        "<figcaption>The crayon is 6 cubes long. It is also 3 paper clips long.</figcaption></figure>"
        "<h2>Centimetres and metres</h2>"
        "<p>Everyone gets the same answer with centimetres (cm) and metres (m). "
        "Use cm for small things and m for long things. <b>100 cm = 1 m</b>.</p>"
        + table(["Unit", "About as long as", "Good for"], [
            ["1 cm", "the width of your fingertip", "crayons, pencils, leaves"],
            ["1 m = 100 cm", "one big step, or a metre stick", "the classroom, the hallway, the gym"],
        ]) +
        "<h2>Read a ruler from 0</h2>"
        "<p>Put one end of the object at the <b>0</b> mark. Look where the other end stops. "
        "Each space between two marks is 1 cm. Count the spaces, not the marks.</p>"
        "<figure class='sn-fig'>" + ruler_svg([("pencil", 0, 6)]) +
        "<figcaption>The pencil starts at 0 and ends at 6. It covers 6 spaces, so it is 6 cm long.</figcaption></figure>"
        "<h2>When the object does not start at 0</h2>"
        "<p>Count the spaces from where the object starts to where it ends. Or subtract: end − start.</p>"
        "<figure class='sn-fig'>" + ruler_svg([("leaf", 3, 10)]) +
        "<figcaption>The leaf starts at 3 and ends at 10. 10 − 3 = 7, so the leaf is 7 cm long, not 10.</figcaption></figure>"
        + ex("Example", "A crayon starts at 2 and ends at 6. How long is it?",
             "Count from 2: 3, 4, 5, 6 is 4 spaces. 6 − 2 = 4.", "4 cm")
        + ex("Draw a line", "Draw a line 5 cm long.",
             "Start at 0. Draw to 5. The line covers 5 spaces.", "Stop at the 5 mark")
        + ex("How much longer?", "A ribbon is 45 cm long. A string is 28 cm long. How much longer is the ribbon?",
             "Subtract: 45 − 28 = 17. Check: 28 + 17 = 45.", "17 cm")
        + "<h2>Common mistakes</h2>"
        + table(["Mistake", "What to do instead"], [
            ["Counting the marks (7 marks for 6 cm)", "Count the spaces between the marks"],
            ["Starting at 1 or at the edge of the ruler", "Line up the end of the object with 0"],
            ["Reading the end number when the object starts at 3", "Subtract the start: 10 − 3 = 7"],
            ["Leaving gaps between cubes", "Push the units together so they touch"],
            ["Thinking a bigger unit gives a bigger number", "Smaller units give a bigger number"],
            ["Saying a pencil is 18 m long", "Picture a fingertip (1 cm) and a big step (1 m)"],
        ])
    )


FAQ = [
    {"q": "What do Grade 2 students learn about length in the Ontario math curriculum?",
     "a": "They measure with non-standard units and see that a smaller unit gives a bigger number (E2.1). "
          "They use centimetres and metres with benchmarks (E2.2) and measure and draw lengths with a ruler, "
          "even when the object does not start at 0 (E2.3)."},
    {"q": "How many centimetres are in a metre?",
     "a": "There are 100 centimetres in 1 metre. A fingertip is about 1 cm wide, and one big step is about 1 m."},
    {"q": "Why does my child get the wrong length on a ruler?",
     "a": "The most common mistakes are counting the marks instead of the spaces, starting at 1, and reading the end "
          "number when the object does not start at 0. Ask your child to count the spaces, or to subtract: end − start."},
    {"q": "How can I practise measuring length at home?",
     "a": "Measure toys and books with LEGO bricks or paper clips, then with a ruler in centimetres. "
          "Guess first, then check. Use big steps to measure a room in metres."},
]


def gen():
    rnd = random.Random(42814)
    P = People(rnd)
    sets = [set_units(P), set_cm_m(P), set_from_zero(P), set_not_zero(P), set_problems(P)]
    balance(sets, rnd)
    seen = set()
    for s in sets:
        assert len(s["items"]) == 20, (s["title"], len(s["items"]))
        assert sorted(it["a"] for it in s["items"]) == sorted([0, 1, 2, 3] * 5), s["title"]
        for it in s["items"]:
            assert len(set(it["c"])) == 4, it
            assert it["q"].count("<svg") <= 1
            assert it["q"] not in seen, it["q"]
            seen.add(it["q"])
            for c in it["c"]:
                assert not re.search(r"\b1 (cubes|paper clips)\b", c), c
                assert not re.search(r"\b([02-9]|\d\d+) (cube|paper clip)\b", c), c
    # ruler pictures with one object: the answer is end − start
    n = 0
    for s in sets:
        for it in s["items"]:
            m = re.search(r"aria-label='([a-z ]+) from (\d+) to (\d+) above a ruler", it["q"])
            if m and " and " not in m.group(1) and m.group(1) != "line":
                assert it["c"][it["a"]] == "%d cm" % (int(m.group(3)) - int(m.group(2))), it["q"][-80:]
                n += 1
            m = re.search(r"aria-label='([a-z ]+) (\d+) (cubes|paper clips) long, above", it["q"])
            if m:
                unit = "cube" if m.group(3) == "cubes" else "clip"
                assert it["c"][it["a"]] == u(int(m.group(2)), unit)
                n += 1
            m = re.search(r"aria-label='([a-z ]+) measured with (\d+) cubes and with (\d+) paper clips", it["q"])
            if m:
                assert it["c"][it["a"]] == m.group(3) + " paper clips"
                n += 1
            m = re.search(r"aria-label='(\w+) from 0 to (\d+) and (\w+) from 0 to (\d+) above", it["q"])
            if m and "How much longer" in it["q"]:
                assert it["c"][it["a"]] == "%d cm" % (int(m.group(2)) - int(m.group(4)))
                n += 1
    assert n == 14 + 12 + 9 + 2 + 4, n
    u_ = {
        "country": "ca-on", "subject": "math", "grade": "grade-2", "slug": "measuring-length", "sort": 14,
        "updated": UPDATED, "pdf_url": "",
        "title": "Measuring Length: Centimetres, Metres and Using a Ruler",
        "seo_title": "Grade 2 Measuring Length Math Worksheets: Centimetres, Metres and Rulers, Free with Answer Key (Ontario)",
        "short_title": "Measuring length",
        "domain": "Spatial Sense",
        "standard_code": "Grade 2: E2.3",
        "standard_url": "https://www.dcp.edu.gov.on.ca/en/curriculum/elementary-mathematics",
        "standard_text": "Measure and draw lengths in centimetres and metres, using a measuring tool, and recognize the "
                         "impact of starting at points other than zero",
        "meta_desc": "Free Grade 2 math worksheets on measuring length for the Ontario curriculum: measure with cubes and "
                     "paper clips, choose centimetres or metres, read a ruler from 0 and from other points, draw lines, "
                     "and solve word problems. 100 questions with an answer key.",
        "key_big": "Line up the object at 0 and count the spaces, not the marks.",
        "key_sub": "If it starts at 3 and ends at 10, it is 10 − 3 = 7 cm long. 100 cm = 1 m. "
                   "A smaller unit gives a bigger number.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }
    return u_


if __name__ == "__main__":
    out = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, out["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(out, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
