# -*- coding: utf-8 -*-
"""
US Grade 1 Math: Measuring Length (1.MD.A.1, 1.MD.A.2)
  python tools/gen_us_math_g1_measuring.py
Non-standard units only (cubes and paper clips), whole numbers only.
Every object is drawn exactly from one unit boundary to another, and every count,
difference and choice is computed in code.
HTML attributes use single quotes (no backslashes in the JSON).
"""
import json, os, random, re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "us", "math", "grade-1")
UPDATED = "2026-11-02"
GREEN = "#006633"
INK = "#2b2b2b"
GREY = "#8a8a8a"
FONT = "Arial, Helvetica, sans-serif"
GIRLS = ["Maya", "Ava", "Mia", "Zoe", "Lily", "Emma", "Nora", "Ruby", "Sofia", "Grace"]
BOYS = ["Leo", "Noah", "Eli", "Sam", "Ben", "Omar", "Kai", "Jack", "Luis", "Owen"]

PX = 24                       # one cube = one grid step in the comparison pictures
PU = {"cube": 24, "clip": 48}  # a paper clip is exactly 2 cubes long in every picture
UNAME = {"cube": ("cube", "cubes"), "clip": ("paper clip", "paper clips")}
CUBE_COLORS = ["#e05a6a", "#3d7cc9"]
BAND = 24


def u(n, unit):
    one, many = UNAME[unit]
    return "%d %s" % (n, one if n == 1 else many)


# ------------------------------------------------------------ helpers (same as the Grade 2 units)
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
    return mcq(q, u(L, unit), [u(c, unit) for c in cands if c > 0], e)


def balance(sets, rnd):
    """Spread the correct answers evenly over the 4 positions in every set."""
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


def svg_wrap(w, h, body, label, lg=False):
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


def the(k):
    return "the " + k


# ------------------------------------------------------------ objects (drawn from x0 to x1 in the band yt..yb)
def draw_object(kind, x0, x1, yt, yb):
    ym = (yt + yb) / 2.0
    L = x1 - x0
    s = []
    if kind == "pencil":
        s.append("<rect x='%.1f' y='%.1f' width='9' height='%.1f' fill='#f2a7b5' stroke='%s' stroke-width='1.2'/>" % (x0, yt + 2, yb - yt - 4, INK))
        s.append("<rect x='%.1f' y='%.1f' width='6' height='%.1f' fill='#b8b8b8' stroke='%s' stroke-width='1.2'/>" % (x0 + 9, yt + 1, yb - yt - 2, INK))
        s.append("<rect x='%.1f' y='%.1f' width='%.1f' height='%.1f' fill='#f4c430' stroke='%s' stroke-width='1.2'/>" % (x0 + 15, yt + 1, L - 33, yb - yt - 2, INK))
        s.append("<polygon points='%.1f,%.1f %.1f,%.1f %.1f,%.1f' fill='#e8c79a' stroke='%s' stroke-width='1.2' stroke-linejoin='round'/>"
                 % (x1 - 18, yt + 1, x1 - 18, yb - 1, x1, ym, INK))
        s.append("<polygon points='%.1f,%.1f %.1f,%.1f %.1f,%.1f' fill='%s'/>" % (x1 - 6, ym - 3.6, x1 - 6, ym + 3.6, x1, ym, INK))
    elif kind == "crayon":
        s.append("<rect x='%.1f' y='%.1f' width='%.1f' height='%.1f' rx='3' fill='#3d7cc9' stroke='%s' stroke-width='1.2'/>" % (x0, yt + 2, L - 12, yb - yt - 4, INK))
        s.append("<rect x='%.1f' y='%.1f' width='%.1f' height='%.1f' fill='#9cc3ee'/>" % (x0 + 6, yt + 8, max(L - 26, 4), yb - yt - 16))
        s.append("<polygon points='%.1f,%.1f %.1f,%.1f %.1f,%.1f %.1f,%.1f' fill='#3d7cc9' stroke='%s' stroke-width='1.2' stroke-linejoin='round'/>"
                 % (x1 - 12, yt + 4, x1 - 12, yb - 4, x1, ym + 2.5, x1, ym - 2.5, INK))
    elif kind == "leaf":
        xm = (x0 + x1) / 2
        s.append("<path d='M%.1f %.1f Q%.1f %.1f %.1f %.1f Q%.1f %.1f %.1f %.1f Z' fill='#7cc47f' stroke='%s' stroke-width='1.4'/>"
                 % (x0, ym, xm, yt - 9, x1, ym, xm, yb + 9, x0, ym, GREEN))
        s.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='1.2'/>" % (x0 + 2, ym, x1 - 3, ym, GREEN))
    elif kind == "nail":
        s.append("<rect x='%.1f' y='%.1f' width='4' height='%.1f' fill='#9aa0a6' stroke='%s' stroke-width='1.1'/>" % (x0, yt + 3, yb - yt - 6, INK))
        s.append("<polygon points='%.1f,%.1f %.1f,%.1f %.1f,%.1f %.1f,%.1f %.1f,%.1f' fill='#c3c7cb' stroke='%s' "
                 "stroke-width='1.1' stroke-linejoin='round'/>"
                 % (x0 + 4, ym - 3, x1 - 10, ym - 3, x1, ym, x1 - 10, ym + 3, x0 + 4, ym + 3, INK))
    elif kind == "ribbon":
        s.append("<rect x='%.1f' y='%.1f' width='%.1f' height='%.1f' fill='#e05a6a' stroke='%s' stroke-width='1.2'/>" % (x0, yt + 6, L, yb - yt - 12, INK))
    elif kind == "paper strip":
        s.append("<rect x='%.1f' y='%.1f' width='%.1f' height='%.1f' fill='#cfe3f7' stroke='%s' stroke-width='1.2'/>" % (x0, yt + 4, L, yb - yt - 8, INK))
    elif kind == "craft stick":
        s.append("<rect x='%.1f' y='%.1f' width='%.1f' height='%.1f' rx='8' fill='#e6c88f' stroke='%s' stroke-width='1.2'/>" % (x0, yt + 4, L, yb - yt - 8, INK))
    elif kind == "eraser":
        s.append("<rect x='%.1f' y='%.1f' width='%.1f' height='%.1f' rx='3' fill='#f2a7b5' stroke='%s' stroke-width='1.2'/>" % (x0, yt + 2, L, yb - yt - 4, INK))
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
        r = (yb - yt) / 2.0 - 1
        s.append("<rect x='%.1f' y='%.1f' width='%.1f' height='6' fill='#e3b94a' stroke='%s' stroke-width='1.2'/>" % (x0 + 2 * r - 2, ym - 3, L - 2 * r + 2, INK))
        for t in range(3):
            s.append("<rect x='%.1f' y='%.1f' width='5' height='%d' fill='#e3b94a' stroke='%s' stroke-width='1.1'/>"
                     % (x1 - 6 - t * 9, ym + 3, 6 - 2 * (t % 2), INK))
        s.append("<circle cx='%.1f' cy='%.1f' r='%.1f' fill='#e3b94a' stroke='%s' stroke-width='1.2'/>" % (x0 + r, ym, r, INK))
        s.append("<circle cx='%.1f' cy='%.1f' r='3' fill='#fff' stroke='%s' stroke-width='1'/>" % (x0 + r * 0.7, ym, INK))
    else:
        raise ValueError(kind)
    return "".join(s)


def guide(x, y0, y1):
    return ("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='1' stroke-dasharray='3 2'/>"
            % (x, y0, x, y1, GREY))


# ------------------------------------------------------------ comparison pictures
PADL = 16


def compare_svg(objs, line=True):
    """objs: list of (kind, start, length) in grid steps. line=True draws the shared start line."""
    gap = 12
    top = 8
    s = []
    right = 0
    for i, (kind, a, L) in enumerate(objs):
        yt = top + i * (BAND + gap)
        x0 = PADL + a * PX
        s.append(draw_object(kind, x0, x0 + L * PX, yt, yt + BAND))
        right = max(right, x0 + L * PX)
    H = top + len(objs) * (BAND + gap) - gap + 8
    if line:
        s.insert(0, "<line x1='%d' y1='2' x2='%d' y2='%d' stroke='%s' stroke-width='2'/>" % (PADL - 2, PADL - 2, H - 2, GREY))
    desc = ", ".join("%s from %d to %d" % (k, a, a + L) for k, a, L in objs)
    return svg_wrap(int(right + 16), int(H), "".join(s), "objects side by side: " + desc)


def tall_svg(objs):
    """objs: list of (kind, length). The objects stand up on one floor line."""
    ph = 16
    maxL = max(L for _, L in objs)
    base = 8 + maxL * ph
    step = 56
    s = []
    for i, (kind, L) in enumerate(objs):
        cx = 36 + i * step
        s.append("<g transform='translate(%d %d) rotate(-90)'>%s</g>" % (cx, base, draw_object(kind, 0, L * ph, -12, 12)))
    W = 36 + (len(objs) - 1) * step + 36
    s.append("<line x1='6' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='2.5'/>" % (base + 1, W - 6, base + 1, INK))
    desc = ", ".join("%s %d high" % (k, L) for k, L in objs)
    return svg_wrap(W, base + 8, "".join(s), "objects standing on the floor: " + desc)


# ------------------------------------------------------------ unit pictures
def cube(x, y, i):
    col = CUBE_COLORS[i % 2]
    return ("<rect x='%.1f' y='%.1f' width='%d' height='%d' fill='%s' stroke='%s' stroke-width='1.2'/>"
            "<rect x='%.1f' y='%.1f' width='%d' height='%d' fill='none' stroke='#ffffff' stroke-opacity='0.6' stroke-width='1'/>"
            % (x, y, PU["cube"], BAND, col, INK, x + 6, y + 6, PU["cube"] - 12, BAND - 12))


def unit_row(x0, y, n, unit, mode="exact", shift=0):
    """n units laid from x0. mode: exact (end to end), gap (spaces between), overlap."""
    pu = PU[unit]
    assert not (mode == "overlap" and unit == "cube"), "overlap pictures use paper clips"
    step = {"exact": pu, "gap": pu + 8, "overlap": pu - 12}[mode]
    s = []
    for i in range(n):
        x = x0 + shift + i * step
        if unit == "cube":
            s.append(cube(x, y, i))
        else:
            s.append(draw_object("paper clip", x, x + pu, y, y + BAND))
    return "".join(s), x0 + shift + (n - 1) * step + pu


def measure_block(kind, L, unit, y, total=None, mode="exact", shift=0, x0=PADL, n=None):
    """Object (length L units) with a row of units under it. Returns (svg, right edge, bottom)."""
    pu = PU[unit]
    x1 = x0 + L * pu
    n = n if n is not None else (total or L)
    s = [guide(x0, y - 3, y + 2 * BAND + 8), guide(x1, y - 3, y + 2 * BAND + 8),
         draw_object(kind, x0, x1, y, y + BAND)]
    row, rr = unit_row(x0, y + BAND + 6, n, unit, mode, shift)
    s.append(row)
    return "".join(s), max(x1, rr), y + 2 * BAND + 8


def measure_svg(kind, L, unit, total=None):
    body, right, bottom = measure_block(kind, L, unit, 6, total)
    lab = "%s %d %s long, above %d %s laid end to end" % (kind, L, UNAME[unit][1], total or L, UNAME[unit][1])
    return svg_wrap(int(right + PADL), int(bottom + 4), body, lab, lg=True)


def n_gap(L, unit):
    """How many units fit with gaps without going past the end of the object."""
    pu = PU[unit]
    return (L * pu + 8) // (pu + 8)


def n_over(L, unit):
    """Overlapping paper clips that end exactly at the end of the object."""
    pu = PU[unit]
    assert ((L - 1) * pu) % (pu - 12) == 0, L
    return (L - 1) * pu // (pu - 12) + 1


def wrong_svg(kind, L, unit, mode):
    """One way of measuring: exact, gap, overlap, late (units start inside the object), early (start before it)."""
    pu = PU[unit]
    if mode == "exact":
        body, right, bottom = measure_block(kind, L, unit, 6)
    elif mode == "gap":
        body, right, bottom = measure_block(kind, L, unit, 6, mode="gap", n=n_gap(L, unit))
    elif mode == "overlap":
        body, right, bottom = measure_block(kind, L, unit, 6, mode="overlap", n=n_over(L, unit))
    elif mode == "late":
        body, right, bottom = measure_block(kind, L, unit, 6, shift=pu // 2, n=L)
    else:   # early: the row begins half a unit before the object
        body, right, bottom = measure_block(kind, L, unit, 6, shift=-(pu // 2), x0=PADL + pu // 2, n=L)
    return svg_wrap(int(right + PADL), int(bottom + 4), body, "%s measured with %s: %s" % (kind, UNAME[unit][1], mode), lg=True)


def ab_svg(kind, L, unit, modes):
    """Two ways to measure the same object, labeled A and B."""
    s = []
    y = 6
    right = 0
    for lab, mode in zip("AB", modes):
        pu = PU[unit]
        if mode == "exact":
            b, r, bt = measure_block(kind, L, unit, y, x0=40)
        elif mode == "gap":
            b, r, bt = measure_block(kind, L, unit, y, x0=40, mode="gap", n=n_gap(L, unit))
        elif mode == "overlap":
            b, r, bt = measure_block(kind, L, unit, y, x0=40, mode="overlap", n=n_over(L, unit))
        else:
            b, r, bt = measure_block(kind, L, unit, y, x0=40, shift=pu // 2, n=L)
        s.append("<text x='10' y='%d' font-size='18' font-weight='700' fill='%s'>%s</text>" % (y + BAND + 8, INK, lab))
        s.append(b)
        right = max(right, r)
        y = bt + 14
    return svg_wrap(int(right + PADL), int(y - 10), "".join(s),
                    "two ways to measure a %s: A %s, B %s" % (kind, modes[0], modes[1]), lg=True)


def two_units_svg(kind, cubes):
    """The same object measured with cubes (top row) and with paper clips (bottom row)."""
    assert cubes % 2 == 0
    x0, x1 = PADL, PADL + cubes * PU["cube"]
    s = [guide(x0, 3, 6 + 3 * BAND + 18), guide(x1, 3, 6 + 3 * BAND + 18), draw_object(kind, x0, x1, 6, 6 + BAND)]
    r1, e1 = unit_row(x0, 6 + BAND + 6, cubes, "cube")
    r2, e2 = unit_row(x0, 6 + 2 * BAND + 12, cubes // 2, "clip")
    assert e1 == x1 and e2 == x1
    s += [r1, r2]
    return svg_wrap(int(x1 + PADL), int(6 + 3 * BAND + 20), "".join(s),
                    "%s measured with %d cubes and with %d paper clips" % (kind, cubes, cubes // 2), lg=True)


def measure2_svg(objs, unit):
    """Two objects, each with its own row of units, both starting at the same line."""
    s = []
    y = 6
    right = 0
    for kind, L in objs:
        b, r, bt = measure_block(kind, L, unit, y)
        s.append(b)
        right = max(right, r)
        y = bt + 12
    desc = " and ".join("%s %d %s" % (k, L, UNAME[unit][1]) for k, L in objs)
    return svg_wrap(int(right + PADL), int(y - 8), "".join(s), "two objects measured: " + desc, lg=True)


# ============================================================ set 1: longer, shorter, taller
def set_compare(P):
    its = []
    OTHER = ["They are the same.", "You cannot tell."]

    def two(objs, ask, picture, up=False):
        (a, la), (b, lb) = objs
        names = [the(a), the(b)]
        if la == lb:
            right = "They are the same."
            e = "Both start at the same line, and both end at the same place. They are <b>the same length</b>."
            if ask == "shorter":
                e += " Neither one is shorter."
            return mcq(fig(picture) + "Which is %s?" % ask, right, names + ["You cannot tell."], e)
        big, small = (a, b) if la > lb else (b, a)
        word = ask
        win = big if ask in ("longer", "taller") else small
        lose = small if win == big else big
        if not up:
            e = ("Both start at the same line. Look at the other end. The %s goes farther, so it is longer. "
                 "The <b>%s is %s</b>." % (big, win, word))
        else:
            e = ("Both stand on the floor. Look at the tops. The %s reaches higher, so it is taller. "
                 "The <b>%s is %s</b>." % (big, win, word))
        return mcq(fig(picture) + "Which is %s?" % ask, the(win), [the(lose)] + OTHER, e)

    # aligned, horizontal
    for objs, ask in [((("pencil", 9), ("crayon", 5)), "longer"), ((("ribbon", 6), ("straw", 10)), "longer"),
                      ((("nail", 5), ("pencil", 8)), "shorter"), ((("key", 3), ("marker", 7)), "longer"),
                      ((("paper strip", 11), ("crayon", 6)), "shorter"), ((("eraser", 3), ("ribbon", 7)), "shorter"),
                      ((("crayon", 6), ("key", 6)), "longer"), ((("craft stick", 8), ("leaf", 4)), "longer"),
                      ((("caterpillar", 6), ("straw", 9)), "shorter"), ((("ribbon", 8), ("pencil", 8)), "shorter")]:
        its.append(two(objs, ask, compare_svg([(k, 0, L) for k, L in objs])))

    # standing up
    for objs, ask in [((("pencil", 8), ("crayon", 5)), "taller"), ((("marker", 6), ("straw", 9)), "taller"),
                      ((("craft stick", 7), ("crayon", 4)), "shorter"), ((("nail", 4), ("pencil", 7)), "shorter")]:
        its.append(two(objs, ask, tall_svg(list(objs)), up=True))

    # not lined up: the shorter object ends farther to the right
    for (a, la), (b, sb, lb) in [(("pencil", 7), ("crayon", 4, 5)), (("ribbon", 8), ("straw", 5, 6)),
                                 (("marker", 7), ("craft stick", 5, 4))]:
        assert la > lb and sb + lb > la
        q = fig(compare_svg([(a, 0, la), (b, sb, lb)], line=False)) + "The two do not start at the same place. Which is longer?"
        e = ("The %s ends farther to the right, but it starts later. Slide it to the left so the ends line up. "
             "Then the %s sticks out past it. The <b>%s is longer</b>." % (b, a, a))
        its.append(mcq(q, the(a), [the(b)] + OTHER, e))

    its.append(mcq("You want to see which pencil is longer. What should you do first?", "Line up the ends.",
                   ["Look at the colors.", "Count the pencils.", "Look at the tips only."],
                   "Put the pencils side by side and <b>line up one end</b>. Then look at the other end. "
                   "The one that sticks out is longer."))
    its.append(mcq("A rope is longer than a stick. Which is true?", "The stick is shorter.",
                   ["The stick is longer.", "The rope is shorter.", "They are the same."],
                   "If the rope is longer than the stick, then the stick is <b>shorter</b> than the rope. "
                   "It is the same fact said the other way."))
    nm, he, his = P.next()
    m = P.next()
    its.append(mcq("%s and %s stand back to back. %s's head is higher. Who is taller?" % (nm, m[0], nm), nm,
                   [m[0], "They are the same.", "You cannot tell."],
                   "They stand on the same floor, so their feet line up. The head that is higher belongs to the taller child. "
                   "<b>%s is taller</b>." % nm))
    order = [0, 1, 2, 3, 6, 4, 5, 7, 8, 9, 10, 11, 12, 13, 17, 14, 15, 16, 18, 19]
    its = [its[i] for i in order]
    assert len(its) == 20, len(its)
    return {"title": "Longer, shorter, taller", "items": its}


# ============================================================ set 2: order three objects
def joined(xs):
    return ", ".join(xs)


def order_choices(names, lens, longest_first=True):
    """names in the correct order + the reverse + two other orders."""
    srt = [n for _, n in sorted(zip(lens, names), reverse=longest_first)]
    a, b, c = srt
    right = joined(srt)
    return right, [joined([c, b, a]), joined([b, a, c]), joined([a, c, b]), joined([c, a, b])]


def set_order(P):
    its = []
    F = [(("straw", 10), ("key", 3), ("pencil", 7), "longest"),
         (("crayon", 5), ("ribbon", 9), ("eraser", 3), "shortest"),
         (("marker", 6), ("paper strip", 11), ("leaf", 4), "longest"),
         (("nail", 5), ("craft stick", 8), ("caterpillar", 3), "shortest"),
         (("pencil", 9), ("ribbon", 11), ("crayon", 6), "longest"),
         (("key", 4), ("straw", 7), ("marker", 5), "shortest")]
    for x, y, z, ask in F:
        objs = [x, y, z]
        lens = [L for _, L in objs]
        names = [k for k, _ in objs]
        best = names[lens.index(max(lens) if ask == "longest" else min(lens))]
        mid = sorted(objs, key=lambda t: t[1])[1][0]
        q = fig(compare_svg([(k, 0, L) for k, L in objs])) + "Which is the %s?" % ask
        e = ("All three start at the same line. Look at where each one ends. The <b>%s</b> is the %s. "
             "The %s is in the middle." % (best, ask, mid))
        its.append(mcq(q, the(best), [the(n) for n in names if n != best] + ["They are the same."], e))

    G = [((("pencil", 6), ("straw", 10), ("eraser", 3)), True),
         ((("ribbon", 8), ("key", 4), ("crayon", 6)), True),
         ((("leaf", 5), ("marker", 7), ("craft stick", 11)), True),
         ((("caterpillar", 9), ("nail", 4), ("paper strip", 6)), True),
         ((("crayon", 7), ("ribbon", 4), ("straw", 9)), False),
         ((("marker", 5), ("pencil", 10), ("key", 3)), False)]
    for objs, lf in G:
        names = [k for k, _ in objs]
        lens = [L for _, L in objs]
        right, wrong = order_choices(names, lens, lf)
        srt = right.split(", ")
        if lf:
            q = fig(compare_svg([(k, 0, L) for k, L in objs])) + "Put them in order from longest to shortest."
            e = ("Find the longest first: the %s. Then the next: the %s. Last is the shortest: the %s. "
                 "So the order is <b>%s</b>." % (srt[0], srt[1], srt[2], right))
        else:
            q = fig(compare_svg([(k, 0, L) for k, L in objs])) + "Put them in order from shortest to longest."
            e = ("Start with the shortest: the %s. Then the %s. Last is the longest: the %s. "
                 "So the order is <b>%s</b>. Do not start with the longest." % (srt[0], srt[1], srt[2], right))
        its.append(mcq(q, right, wrong, e))

    its.append(mcq("The rope is longer than the stick. The stick is longer than the pencil. Which is the longest?",
                   "the rope", ["the stick", "the pencil", "You cannot tell."],
                   "The rope is longer than the stick, and the stick is longer than the pencil. "
                   "So the order is rope, stick, pencil. <b>The rope</b> is the longest."))
    its.append(mcq("The bus is longer than the car. The car is longer than the bike. Which is the shortest?",
                   "the bike", ["the bus", "the car", "You cannot tell."],
                   "The order from longest is bus, car, bike. <b>The bike</b> is the shortest."))
    its.append(mcq("The ribbon is shorter than the yarn. The yarn is shorter than the rope. Which is the longest?",
                   "the rope", ["the ribbon", "the yarn", "You cannot tell."],
                   "Each one is shorter than the next. From shortest: ribbon, yarn, rope. "
                   "So <b>the rope</b> is the longest. Read “shorter” carefully."))
    its.append(mcq("The cat is shorter than the dog. The dog is shorter than the horse. Which animal is in the middle?",
                   "the dog", ["the cat", "the horse", "You cannot tell."],
                   "From shortest to tallest: cat, dog, horse. <b>The dog</b> is in the middle."))
    a, b, c = P.next(), P.next(), P.next()
    its.append(mcq("%s is taller than %s. %s is taller than %s. Who is the shortest?" % (a[0], b[0], b[0], c[0]),
                   c[0], [a[0], b[0], "You cannot tell."],
                   "%s is taller than %s, and %s is taller than %s. From tallest: %s, %s, %s. "
                   "<b>%s</b> is the shortest." % (a[0], b[0], b[0], c[0], a[0], b[0], c[0], c[0])))
    nm, he, his = P.next()
    its.append(mcq("%s cannot move %s desk to the door. %s uses a string. The string is as long as the desk. "
                   "The string is shorter than the door. Which is longer?" % (nm, his, cap(he)),
                   "the door", ["the desk", "They are the same.", "You cannot tell."],
                   "The string is the same length as the desk. The door is longer than the string, "
                   "so the door is longer than the desk too. <b>The door</b> is longer."))
    nm, he, his = P.next()
    its.append(mcq("%s has a string. It is as long as %s book. The string is longer than %s pencil. "
                   "Which is longer, the book or the pencil?" % (nm, his, his),
                   "the book", ["the pencil", "They are the same.", "You cannot tell."],
                   "The book and the string are the same length. The string is longer than the pencil. "
                   "So <b>the book</b> is longer than the pencil."))
    its.append(mcq("The green snake is longer than the blue snake. The red snake is shorter than the blue snake. "
                   "Which list goes from longest to shortest?",
                   "green, blue, red", ["red, blue, green", "blue, green, red", "green, red, blue"],
                   "Green is longer than blue. Red is shorter than blue. So blue is in the middle: "
                   "<b>green, blue, red</b>."))
    assert len(its) == 20, len(its)
    return {"title": "Order three objects by length", "items": its}


# ============================================================ set 3: measure with cubes and paper clips
S3 = [("crayon", 4, "cube", None), ("key", 3, "cube", None), ("pencil", 7, "cube", None),
      ("eraser", 2, "clip", None), ("ribbon", 5, "cube", None), ("leaf", 3, "clip", None),
      ("straw", 9, "cube", None), ("marker", 4, "clip", None), ("caterpillar", 6, "cube", None),
      ("paper strip", 5, "clip", None), ("craft stick", 8, "cube", None), ("pencil", 6, "clip", None),
      ("nail", 5, "cube", 8), ("crayon", 3, "clip", 5), ("worm", 7, "cube", 10), ("ribbon", 4, "clip", 6),
      ("marker", 11, "cube", None), ("straw", 6, "clip", None)]


def set_units(P):
    its = []
    asks = ["How many %s long is the %s?", "Count the %s. How long is the %s?", "How long is the %s?"]
    for i, (kind, L, unit, total) in enumerate(S3):
        if total:
            q = "Count only the %s under the %s. How long is the %s?" % (UNAME[unit][1], kind, kind)
        elif i % 3 == 2:
            q = asks[2] % kind
        else:
            q = asks[i % 3] % (UNAME[unit][1], kind)
        q = fig(measure_svg(kind, L, unit, total)) + q
        e = "Count the %s from one end of the %s to the other: %s. It is <b>%s</b> long." % (
            UNAME[unit][1], kind, count_list(L), u(L, unit))
        if total:
            e += " There are %d %s in the row, but only %d are under the %s. Do not count the extra ones." % (
                total, UNAME[unit][1], L, kind)
            cands = [total, L + 1, L - 1]
        else:
            e += " Touch each one as you count so you do not skip one or count one twice."
            cands = [L + 1, L - 1, L + 2]
        its.append(mcq_len(q, L, unit, cands, e))
        if i == 5:
            its.append(mcq("You measure a crayon with cubes. What do you count?", "the cubes under it",
                           ["all the cubes in the box", "the spaces between cubes", "the colors of the cubes"],
                           "Lay cubes along the crayon from end to end. Count only <b>the cubes under the crayon</b>. "
                           "That number is its length."))
        if i == 11:
            nm, he, his = P.next()
            its.append(mcq_len("%s lays cubes along %s book, end to end, with no gaps. %s uses 9 cubes. How long is the book?"
                               % (nm, his, cap(he)), 9, "cube", [10, 8, 11],
                               "%s used 9 cubes from one end of the book to the other. So the book is <b>9 cubes</b> long." % nm))
    assert len(its) == 20, len(its)
    return {"title": "Measure with cubes and paper clips", "items": its}


# ============================================================ set 4: measure the right way
OK = "Yes, it is right."
GAP = "No, there are gaps."
OVER = "No, they overlap."
START = "No, the start is wrong."
MODE_ANS = {"exact": OK, "gap": GAP, "overlap": OVER, "late": START, "early": START}


def set_right_way(P):
    its = []
    W = [("pencil", 7, "cube", "exact"), ("crayon", 4, "clip", "gap"), ("ribbon", 7, "clip", "overlap"),
         ("straw", 6, "cube", "late"), ("marker", 5, "clip", "exact"), ("craft stick", 9, "cube", "gap"),
         ("paper strip", 4, "clip", "overlap"), ("pencil", 3, "clip", "early")]
    for kind, L, unit, mode in W:
        q = fig(wrong_svg(kind, L, unit, mode)) + "Is this the right way to measure the %s?" % kind
        un = UNAME[unit][1]
        if mode == "exact":
            e = ("Yes. The %s start at one end of the %s and go to the other end. They touch with no gaps "
                 "and no overlaps. The %s is <b>%s</b> long." % (un, kind, kind, u(L, unit)))
        elif mode == "gap":
            e = ("<b>No, there are gaps</b> between the %s. The empty spaces are not counted, so the number would be too small. "
                 "Push the %s together so they touch." % (un, un))
        elif mode == "overlap":
            e = ("<b>No, the %s overlap</b>. They lie on top of each other, so you would count too many. "
                 "Lay them end to end, side by side." % un)
        elif mode == "late":
            e = ("<b>No, the start is wrong.</b> The first %s does not start at the end of the %s. "
                 "Line up the first one with the end of the %s." % (UNAME[unit][0], kind, kind))
        else:
            e = ("<b>No, the start is wrong.</b> The first %s sticks out before the %s starts. "
                 "Line up the first one with the end of the %s." % (UNAME[unit][0], kind, kind))
        its.append(mcq(q, MODE_ANS[mode], [x for x in [OK, GAP, OVER, START] if x != MODE_ANS[mode]], e))

    for kind, L, unit, modes, right in [("crayon", 5, "cube", ("gap", "exact"), "B"),
                                         ("ribbon", 4, "clip", ("exact", "overlap"), "A"),
                                         ("pencil", 6, "cube", ("late", "gap"), "neither")]:
        q = fig(ab_svg(kind, L, unit, modes)) + "Which picture shows the right way to measure?"
        why = {"gap": "has gaps", "overlap": "has %s on top of each other" % UNAME[unit][1],
               "late": "does not start at the end of the %s" % kind, "exact": "is right"}
        e = "Picture A %s. Picture B %s. " % (why[modes[0]], why[modes[1]])
        if right == "neither":
            e += "So <b>neither</b> picture is right. The %s must touch end to end, from one end to the other." % UNAME[unit][1]
        else:
            e += "So <b>%s</b> is the right way: no gaps, no overlaps, and it starts at the end." % right
        its.append(mcq(q, right, [x for x in ["A", "B", "both", "neither"] if x != right], e))

    q = fig(two_units_svg("crayon", 6)) + "The crayon is 6 cubes long. How many paper clips long is it?"
    its.append(mcq_len(q, 3, "clip", [6, 12, 4],
                       "Look at the bottom row. Count the paper clips under the crayon: 1, 2, 3. It is <b>3 paper clips</b> long. "
                       "A paper clip is longer than a cube, so you need fewer of them."))
    q = fig(two_units_svg("ribbon", 8)) + "The ribbon is 8 cubes long but only 4 paper clips long. Why?"
    its.append(mcq(q, "A cube is shorter.", ["A cube is longer.", "The ribbon grew.", "Someone counted wrong."],
                   "Both are right. <b>A cube is shorter than a paper clip</b>, so it takes more cubes to cover the same ribbon."))
    q = fig(two_units_svg("pencil", 10)) + "Which is true about the pencil?"
    its.append(mcq(q, "10 cubes and 5 clips", ["5 cubes and 10 clips", "10 cubes and 10 clips", "5 cubes and 5 clips"],
                   "Count each row. 10 cubes fit under the pencil, and 5 paper clips fit under it. "
                   "So it is <b>10 cubes and 5 paper clips</b> long. Same pencil, two units."))

    nm, he, his = P.next()
    m = P.next()
    its.append(mcq("%s measures a book with paper clips and gets 4. %s measures the same book with cubes. "
                   "A cube is shorter than a paper clip. What will %s get?" % (nm, m[0], m[1]),
                   "more than 4", ["less than 4", "exactly 4", "You cannot tell."],
                   "Cubes are shorter, so it takes <b>more</b> of them to cover the same book. The number will be more than 4."))
    nm, he, his = P.next()
    m = P.next()
    its.append(mcq("%s's stick is 5 paper clips long. %s's stick is 5 cubes long. A paper clip is longer than a cube. "
                   "Whose stick is longer?" % (nm, m[0]),
                   "%s's stick" % nm, ["%s's stick" % m[0], "They are the same.", "You cannot tell."],
                   "The numbers are the same, but the units are not. A paper clip is longer than a cube, "
                   "so 5 paper clips is longer than 5 cubes. <b>%s's stick</b> is longer." % nm))
    its.append(mcq("What should you use to measure a pencil?", "cubes all the same size",
                   ["big and small cubes mixed", "just 1 cube", "cubes with gaps"],
                   "Every unit must be <b>the same size</b>. If some cubes are big and some are small, the count does not tell the length."))
    its.append(mcq("Where should you put the first cube?", "at one end",
                   ["in the middle", "a little past the end", "anywhere"],
                   "Put the first cube right <b>at one end</b> of the object. Then lay the next cubes end to end until you reach the other end."))
    nm, he, his = P.next()
    its.append(mcq("%s measures a stick with 7 cubes, but %s leaves gaps between them. How long is the stick really?" % (nm, he),
                   "more than 7 cubes", ["less than 7 cubes", "exactly 7 cubes", "You cannot tell."],
                   "The gaps are part of the stick too, but no cube is there. If %s pushes the cubes together, "
                   "more cubes will fit. The stick is <b>more than 7 cubes</b> long." % nm))
    nm, he, his = P.next()
    its.append(mcq("%s's paper clips overlap on a ribbon. %s counts 6. How long is the ribbon really?" % (nm, cap(he)),
                   "less than 6 clips", ["more than 6 clips", "exactly 6 clips", "You cannot tell."],
                   "When paper clips overlap, too many fit on the ribbon. Laid end to end, fewer would fit. "
                   "The ribbon is <b>less than 6 paper clips</b> long."))
    order = [0, 1, 2, 3, 4, 5, 6, 7, 17, 16, 8, 9, 10, 18, 19, 11, 12, 13, 14, 15]
    its = [its[i] for i in order]
    assert len(its) == 20, len(its)
    return {"title": "Measure the right way", "items": its}


# ============================================================ set 5: word problems
def diff_e(a, b, unit, d):
    e = "Subtract the shorter length from the longer one: %d − %d = <b>%d</b>. " % (a, b, d)
    if 2 <= d <= 5:
        e += "Or count up from %d to %d: %s. That is %d. " % (b, a, count_list(d, b + 1), d)
    e += "Do not add: %d + %d = %d is how long they are together." % (a, b, a + b)
    return e


def set_word(P):
    its = []
    F = [("cube", "pencil", 9, "crayon", 5, "longer"), ("clip", "straw", 5, "key", 2, "longer"),
         ("cube", "ribbon", 10, "eraser", 3, "longer"), ("cube", "marker", 7, "caterpillar", 4, "shorter"),
         ("clip", "paper strip", 6, "crayon", 3, "shorter"), ("cube", "craft stick", 11, "nail", 5, "longer"),
         ("clip", "ribbon", 5, "leaf", 4, "longer"), ("cube", "straw", 12, "pencil", 8, "shorter")]
    for unit, A, a, B, b, ask in F:
        d = a - b
        q = fig(measure2_svg([(A, a), (B, b)], unit))
        un = UNAME[unit][1]
        if ask == "longer":
            q += "How many %s longer is the %s than the %s?" % (un, A, B)
        else:
            q += "How many %s shorter is the %s than the %s?" % (un, B, A)
        e = "The %s is %s. The %s is %s. " % (A, u(a, unit), B, u(b, unit)) + diff_e(a, b, unit, d)
        its.append(mcq_len(q, d, unit, [a + b, a, d + 1, d - 1], e))

    W = [("{N}'s clay snake is 9 cubes long. {M}'s clay snake is 6 cubes long. How many cubes longer is {N}'s snake?", 9, 6, "cube", "diff"),
         ("{N} made a cube train 12 cubes long. {M}'s train is 7 cubes long. How many cubes shorter is {M}'s train?", 12, 7, "cube", "diff"),
         ("{N}'s book is 6 paper clips long. {His} desk is 15 paper clips long. How many paper clips longer is the desk?", 15, 6, "clip", "diff"),
         ("A worm is 4 cubes long. A snake is 13 cubes long. How many cubes longer is the snake?", 13, 4, "cube", "diff"),
         ("{N}'s shoe is 7 cubes long. {M}'s shoe is 9 cubes long. How many cubes longer is {M}'s shoe?", 9, 7, "cube", "diff"),
         ("A leaf is 8 cubes long. A stick is 17 cubes long. How many cubes shorter is the leaf?", 17, 8, "cube", "diff"),
         ("A toy train is 20 cubes long. A toy car is 6 cubes long. How many cubes longer is the train?", 20, 6, "cube", "diff"),
         ("A red ribbon is 7 paper clips long. A blue ribbon is 3 paper clips longer. How long is the blue ribbon?", 7, 3, "clip", "more"),
         ("{N}'s tower is 11 cubes tall. {M}'s tower is 3 cubes taller. How tall is {M}'s tower?", 11, 3, "cube", "more"),
         ("A pencil is 8 cubes long. A crayon is 2 cubes shorter. How long is the crayon?", 8, 2, "cube", "less"),
         ("{N} puts a 5-cube stick and a 4-cube stick end to end. How long are they together?", 5, 4, "cube", "more"),
         ("{N} wants a tower 16 cubes tall. {His} tower is 9 cubes tall now. How many more cubes does {he} need?", 16, 9, "cube", "diff")]
    for tpl, a, b, unit, kind in W:
        nm, he, his = P.next()
        m = P.next()[0] if "{M}" in tpl else ""
        q = tpl.format(N=nm, M=m, he=he, His=cap(his))
        if kind == "diff":
            d = a - b
            e = diff_e(a, b, unit, d)
            if "more cubes" in tpl:
                e = ("Count up from 9 to 16, or subtract: 16 − 9 = <b>7</b>. %s needs 7 more cubes. "
                     "Check: 9 + 7 = 16." % nm)
            its.append(mcq_len(q, d, unit, [a + b, d + 1, a, d - 1], e))
        elif kind == "more":
            t = a + b
            if "together" in tpl:
                e = "End to end, the lengths join. Add: 5 + 4 = <b>9</b>. Together they are 9 cubes long."
            else:
                w = "taller" if "taller" in tpl else "longer"
                e = ("“%d %s” means add %d. %d + %d = <b>%d</b>. Do not subtract: it is %s, "
                     "so the number must be bigger than %d." % (b, w, b, a, b, t, w, a))
            its.append(mcq_len(q, t, unit, [a - b, a, t + 1, t - 1], e))
        else:
            t = a - b
            e = ("“%d shorter” means take away %d. %d − %d = <b>%d</b>. The crayon is shorter, "
                 "so the number must be smaller than %d." % (b, b, a, b, t, a))
            its.append(mcq_len(q, t, unit, [a + b, a, t + 1, t - 1], e))
    order = [0, 1, 8, 2, 9, 3, 10, 4, 11, 5, 15, 6, 16, 7, 12, 17, 13, 18, 14, 19]
    its = [its[i] for i in order]
    assert len(its) == 20, len(its)
    return {"title": "Word problems: how many longer?", "items": its}


# ============================================================ lesson
def body_html():
    return (
        "<h2>Line up the ends to compare</h2>"
        "<p>To see which is longer, put the two things side by side. Line up one end. "
        "Then look at the other end. The one that sticks out is <b>longer</b>. The other one is <b>shorter</b>.</p>"
        "<figure class='sn-fig'>" + compare_svg([("pencil", 0, 8), ("crayon", 0, 5)]) +
        "<figcaption>Both start at the same line. The pencil sticks out, so the pencil is longer and the crayon is shorter.</figcaption></figure>"
        "<h2>Put three things in order</h2>"
        "<p>Find the longest. Then find the shortest. The last one is in the middle.</p>"
        "<figure class='sn-fig'>" + compare_svg([("ribbon", 0, 6), ("straw", 0, 10), ("key", 0, 3)]) +
        "<figcaption>From longest to shortest: straw, ribbon, key.</figcaption></figure>"
        + ex("Example", "The rope is longer than the stick. The stick is longer than the pencil. Is the rope longer than the pencil?",
             "Put them in order: rope, stick, pencil. The rope is first, so it is longer than the pencil.", "Yes, the rope is longer.")
        + "<h2>Measure with cubes</h2>"
        "<p>Lay cubes along the object, <b>end to end</b>. Start right at one end. Stop at the other end. "
        "Count the cubes. That number is the length.</p>"
        "<figure class='sn-fig'>" + measure_svg("crayon", 6, "cube") +
        "<figcaption>6 cubes fit from one end of the crayon to the other. The crayon is 6 cubes long.</figcaption></figure>"
        "<h2>No gaps, no overlaps</h2>"
        "<p>The cubes must touch. Do not leave spaces. Do not put one cube on top of another. All the cubes must be the same size.</p>"
        "<figure class='sn-fig'>" + ab_svg("pencil", 5, "cube", ("gap", "exact")) +
        "<figcaption>A has gaps, so it is wrong. B is right: the pencil is 5 cubes long.</figcaption></figure>"
        "<h2>Bigger unit, smaller number</h2>"
        "<p>A paper clip is longer than a cube. So the same ribbon is <b>fewer</b> paper clips than cubes.</p>"
        "<figure class='sn-fig'>" + two_units_svg("ribbon", 8) +
        "<figcaption>The same ribbon is 8 cubes long and 4 paper clips long.</figcaption></figure>"
        "<h2>How many longer?</h2>"
        "<p>Measure both with the same unit. Then subtract, or count up from the shorter one.</p>"
        + ex("Example", "A pencil is 9 cubes long. A crayon is 5 cubes long. How many cubes longer is the pencil?",
             "9 − 5 = 4. Or count up from 5: 6, 7, 8, 9. That is 4.", "4 cubes")
        + "<h2>Common mistakes</h2>"
        + table(["Mistake", "What to do instead"], [
            ["Not lining up the ends", "Start both objects at the same line"],
            ["Leaving gaps between cubes", "Push the cubes together so they touch"],
            ["Letting paper clips overlap", "Lay them end to end, side by side"],
            ["Starting past the end of the object", "Put the first cube right at the end"],
            ["Counting cubes that stick out past the end", "Count only the cubes under the object"],
            ["Thinking 5 cubes and 5 paper clips are the same", "A paper clip is longer, so 5 paper clips is longer"],
            ["Adding to find how many longer", "Subtract the shorter length from the longer one"],
        ])
    )


FAQ = [
    {"q": "What do 1st graders learn about measuring length?",
     "a": "In Grade 1, children compare and order objects by length and measure with same-size units such as cubes or paper clips laid end to end. "
          "They learn that the length is the number of units with no gaps or overlaps (Common Core 1.MD.A.1–2)."},
    {"q": "Why do first graders measure with cubes and paper clips instead of rulers?",
     "a": "Laying real units end to end shows what a length is: how many same-size units cover the object. "
          "This idea makes rulers easy to understand in Grade 2."},
    {"q": "Why is an object more cubes long than paper clips long?",
     "a": "A cube is shorter than a paper clip, so it takes more cubes to cover the same object. A ribbon can be 8 cubes and 4 paper clips long at the same time."},
    {"q": "How can you compare two lengths without putting them side by side?",
     "a": "Use a third object, like a string. If the string is as long as the desk and shorter than the door, then the door is longer than the desk."},
]


def gen():
    rnd = random.Random(111)
    P = People(rnd)
    sets = [set_compare(P), set_order(P), set_units(P), set_right_way(P), set_word(P)]
    balance(sets, rnd)
    seen = set()
    for s in sets:
        assert len(s["items"]) == 20, (s["title"], len(s["items"]))
        assert sorted(it["a"] for it in s["items"]) == sorted([0, 1, 2, 3] * 5), s["title"]
        for it in s["items"]:
            assert len(set(it["c"])) == 4, it
            k = it["q"]
            assert k not in seen, it["q"]
            seen.add(k)
            for c in it["c"]:      # singular/plural units
                assert not re.search(r"\b1 (cubes|paper clips|clips)\b", c), c
                assert not re.search(r"\b([02-9]|\d\d+) (cube|paper clip|clip)\b", c), c
    # every one-object picture: the answer is the number of units under the object
    n = 0
    for s in sets:
        for it in s["items"]:
            m = re.search(r"aria-label='([a-z ]+) (\d+) (cubes|paper clips) long, above (\d+)", it["q"])
            if m:
                unit = "cube" if m.group(3) == "cubes" else "clip"
                assert it["c"][it["a"]] == u(int(m.group(2)), unit)
                n += 1
    assert n == 18, n
    return {
        "country": "us", "subject": "math", "grade": "grade-1", "slug": "measuring-length", "sort": 11,
        "updated": UPDATED, "pdf_url": "",
        "title": "Measuring Length: Compare, Order and Measure with Cubes",
        "seo_title": "Grade 1 Measuring Length Worksheets: Longer and Shorter, Order by Length, Measure with Cubes and Paper Clips",
        "short_title": "Measuring length",
        "domain": "Measurement and Data",
        "standard_code": "1.MD.A.2",
        "standard_url": "https://www.thecorestandards.org/Math/Content/1/MD/A/2/",
        "standard_text": "Express the length of an object as a whole number of length units, by laying multiple copies of a shorter object "
                         "(the length unit) end to end; understand that the length measurement of an object is the number of same-size "
                         "length units that span it with no gaps or overlaps. Limit to contexts where the object being measured is spanned "
                         "by a whole number of length units with no gaps or overlaps.",
        "meta_desc": "Free Grade 1 measuring length worksheets with pictures: longer, shorter and taller, order three objects by length, "
                     "measure with cubes and paper clips, no gaps or overlaps, and how many longer. 100 practice questions with answers.",
        "key_big": "Line up the ends, then count the same-size units with no gaps and no overlaps.",
        "key_sub": "To compare, start both objects at the same line. To measure, lay cubes end to end from one end to the other and count them. "
                   "A bigger unit gives a smaller number.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }


if __name__ == "__main__":
    out = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, out["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(out, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
