# -*- coding: utf-8 -*-
"""
CA-ON Grade 1 Math: Comparing length, mass and capacity (Ontario Mathematics Curriculum 2020, E2.1 and E2.2)
  python3 tools/gen_caon_math_g1_measuring.py
Compare and order everyday objects by length, area, mass and capacity; measure length with non-standard units
(cubes, paper clips) laid end to end with no gaps or overlaps.
Every picture is drawn exactly from the data: objects run from one cube boundary to another, a paper clip is
exactly 2 cubes long, the heavier side of a balance is the lower one, water levels are exact and every
shape is made of equal squares.
Wrong answers come from real mistakes: not lining up the ends, gaps and overlaps, mixing units, counting cubes
past the end, thinking bigger means heavier and thinking longer means it covers more.
HTML attributes use single quotes (no backslashes in the JSON).
"""
import json, os, random, re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "ca-on", "math", "grade-1")
UPDATED = "2026-11-02"
GREEN = "#006633"
INK = "#2b2b2b"
GREY = "#8a8a8a"
WATER = "#9fd3f2"
WATER_LINE = "#2a7fb8"
FONT = "Arial, Helvetica, sans-serif"
GIRLS = ["Olivia", "Emma", "Maya", "Zoe", "Amira", "Mei", "Chloe", "Priya", "Leah", "Hana", "Ava", "Sofia"]
BOYS = ["Liam", "Noah", "Aiden", "Lucas", "Owen", "Arjun", "Ethan", "Jayden", "Benjamin", "Mateo", "Nathan", "Kai"]

PX = 24                       # one cube = one grid step in the comparison pictures
PU = {"cube": 24, "clip": 48}  # a paper clip is exactly 2 cubes long in every picture
UNAME = {"cube": ("cube", "cubes"), "clip": ("paper clip", "paper clips")}
CUBE_COLOURS = ["#e05a6a", "#3d7cc9"]
BAND = 24


def u(n, unit):
    one, many = UNAME[unit]
    return "%d %s" % (n, one if n == 1 else many)


# ------------------------------------------------------------ helpers
def mcq(q, correct, cands, e, lock=False):
    """4 choices: correct + the first 3 unique distractors. lock=True keeps the given order (picture labels A-D, shape A/B)."""
    correct = str(correct)
    if lock:
        assert len(cands) == 4 and len(set(cands)) == 4 and correct in cands
        return {"q": q, "c": list(cands), "a": cands.index(correct), "e": e, "lock": True}
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
    """Spread the correct answers evenly (5/5/5/5) in every set. Locked A-D items keep their place."""
    for s in sets:
        need = [5, 5, 5, 5]
        for it in s["items"]:
            if it.get("lock"):
                need[it["a"]] -= 1
        assert min(need) >= 0, (s["title"], need)
        targets = [p for p in range(4) for _ in range(need[p])]
        rnd.shuffle(targets)
        free = [it for it in s["items"] if not it.get("lock")]
        assert len(free) == len(targets)
        for it, t in zip(free, targets):
            c = it["c"]
            right = c[it["a"]]
            wrong = [x for i, x in enumerate(c) if i != it["a"]]
            rnd.shuffle(wrong)
            it["c"] = wrong[:t] + [right] + wrong[t:]
            it["a"] = t
        for it in s["items"]:
            it.pop("lock", None)


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


def text(x, y, t, fs=15, anchor="middle", bold=True, col=INK):
    return ("<text x='%.1f' y='%.1f' font-size='%d'%s fill='%s' text-anchor='%s'>%s</text>"
            % (x, y, fs, " font-weight='700'" if bold else "", col, anchor, t))


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


# ------------------------------------------------------------ length objects (drawn from x0 to x1 in the band yt..yb)
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
    return svg_wrap(int(right + 16), int(H), "".join(s), "objects side by side: " + desc, lg=True)


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
    col = CUBE_COLOURS[i % 2]
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
    pu = PU[unit]
    return (L * pu + 8) // (pu + 8)


def n_over(L, unit):
    pu = PU[unit]
    assert ((L - 1) * pu) % (pu - 12) == 0, L
    return (L - 1) * pu // (pu - 12) + 1


def wrong_svg(kind, L, unit, mode):
    """One way of measuring: exact, gap, overlap, late (units start inside the object)."""
    pu = PU[unit]
    if mode == "exact":
        body, right, bottom = measure_block(kind, L, unit, 6)
    elif mode == "gap":
        body, right, bottom = measure_block(kind, L, unit, 6, mode="gap", n=n_gap(L, unit))
    elif mode == "overlap":
        body, right, bottom = measure_block(kind, L, unit, 6, mode="overlap", n=n_over(L, unit))
    else:
        body, right, bottom = measure_block(kind, L, unit, 6, shift=pu // 2, n=L)
    return svg_wrap(int(right + PADL), int(bottom + 4), body, "%s measured with %s: %s" % (kind, UNAME[unit][1], mode), lg=True)


def two_units_svg(kind, cubes):
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


# ------------------------------------------------------------ things on a balance (bottom centre at cx, b)
SC = 12   # size of one small cube on a balance


def thing(kind, cx, b, n=0):
    s = []
    if kind == "apple":
        s.append("<circle cx='%.1f' cy='%.1f' r='14' fill='#d94b4b' stroke='%s' stroke-width='1.3'/>" % (cx, b - 14, INK))
        s.append("<path d='M%.1f %.1f q1 -6 3 -8' fill='none' stroke='#6b4226' stroke-width='2'/>" % (cx, b - 27))
        s.append("<ellipse cx='%.1f' cy='%.1f' rx='5' ry='2.6' fill='#5aa65a'/>" % (cx + 7, b - 32))
    elif kind == "orange":
        s.append("<circle cx='%.1f' cy='%.1f' r='13' fill='#f39c32' stroke='%s' stroke-width='1.3'/>" % (cx, b - 13, INK))
        s.append("<circle cx='%.1f' cy='%.1f' r='1.6' fill='#5aa65a'/>" % (cx, b - 24))
    elif kind == "pear":
        s.append("<circle cx='%.1f' cy='%.1f' r='13' fill='#b5d55a' stroke='%s' stroke-width='1.3'/>" % (cx, b - 13, INK))
        s.append("<circle cx='%.1f' cy='%.1f' r='8.5' fill='#b5d55a' stroke='%s' stroke-width='1.3'/>" % (cx, b - 29, INK))
        s.append("<circle cx='%.1f' cy='%.1f' r='12' fill='#b5d55a'/>" % (cx, b - 14))
        s.append("<path d='M%.1f %.1f l1 -6' stroke='#6b4226' stroke-width='2'/>" % (cx, b - 37))
    elif kind == "banana":
        s.append("<path d='M%.1f %.1f Q%.1f %.1f %.1f %.1f Q%.1f %.1f %.1f %.1f Z' fill='#f4d03f' stroke='%s' stroke-width='1.3' "
                 "stroke-linejoin='round'/>" % (cx - 30, b - 10, cx, b + 10, cx + 30, b - 10, cx, b - 8, cx - 30, b - 10, INK))
    elif kind == "feather":
        s.append("<path d='M%.1f %.1f Q%.1f %.1f %.1f %.1f Q%.1f %.1f %.1f %.1f Z' fill='#eef2f7' stroke='%s' stroke-width='1.2'/>"
                 % (cx - 28, b - 3, cx - 4, b - 22, cx + 28, b - 12, cx + 2, b + 2, cx - 28, b - 3, INK))
        s.append("<path d='M%.1f %.1f Q%.1f %.1f %.1f %.1f' fill='none' stroke='%s' stroke-width='1.2'/>"
                 % (cx - 30, b - 1, cx, b - 7, cx + 28, b - 12, INK))
    elif kind == "book":
        s.append("<rect x='%.1f' y='%.1f' width='46' height='22' fill='#3d7cc9' stroke='%s' stroke-width='1.3'/>" % (cx - 23, b - 22, INK))
        s.append("<rect x='%.1f' y='%.1f' width='40' height='5' fill='#ffffff' stroke='%s' stroke-width='1'/>" % (cx - 18, b - 8, INK))
    elif kind == "brick":
        s.append("<rect x='%.1f' y='%.1f' width='50' height='22' fill='#b5523b' stroke='%s' stroke-width='1.3'/>" % (cx - 25, b - 22, INK))
        s.append("<path d='M%.1f %.1f h50 M%.1f %.1f v11 M%.1f %.1f v11 M%.1f %.1f v11' stroke='#e8d5c4' stroke-width='1.2'/>"
                 % (cx - 25, b - 11, cx - 8, b - 22, cx + 12, b - 22, cx + 2, b - 11))
    elif kind == "sponge":
        s.append("<rect x='%.1f' y='%.1f' width='44' height='20' rx='3' fill='#f7dc6f' stroke='%s' stroke-width='1.3'/>" % (cx - 22, b - 20, INK))
        for dx, dy in [(-13, -13), (-2, -7), (9, -14), (14, -6), (-12, -5)]:
            s.append("<circle cx='%.1f' cy='%.1f' r='1.8' fill='#c9a227'/>" % (cx + dx, b + dy))
    elif kind == "beach ball":
        s.append("<circle cx='%.1f' cy='%.1f' r='28' fill='#e05a6a'/>" % (cx, b - 28))
        s.append("<ellipse cx='%.1f' cy='%.1f' rx='18' ry='28' fill='#ffffff'/>" % (cx, b - 28))
        s.append("<ellipse cx='%.1f' cy='%.1f' rx='7' ry='28' fill='#3d7cc9'/>" % (cx, b - 28))
        s.append("<circle cx='%.1f' cy='%.1f' r='28' fill='none' stroke='%s' stroke-width='1.3'/>" % (cx, b - 28, INK))
    elif kind == "stone":
        s.append("<path d='M%.1f %.1f Q%.1f %.1f %.1f %.1f Q%.1f %.1f %.1f %.1f Q%.1f %.1f %.1f %.1f Z' fill='#9aa0a6' "
                 "stroke='%s' stroke-width='1.3'/>"
                 % (cx - 16, b, cx - 18, b - 14, cx - 2, b - 17, cx + 16, b - 18, cx + 16, b - 6, cx + 16, b, cx - 16, b, INK))
    elif kind == "pillow":
        s.append("<rect x='%.1f' y='%.1f' width='64' height='28' rx='12' fill='#eef2f7' stroke='%s' stroke-width='1.3'/>" % (cx - 32, b - 28, INK))
        s.append("<path d='M%.1f %.1f q4 4 0 8 M%.1f %.1f q-4 4 0 8' fill='none' stroke='%s' stroke-width='1'/>"
                 % (cx - 22, b - 18, cx + 22, b - 18, GREY))
    elif kind == "can of beans":
        s.append("<rect x='%.1f' y='%.1f' width='26' height='30' fill='#9aa0a6' stroke='%s' stroke-width='1.3'/>" % (cx - 13, b - 30, INK))
        s.append("<rect x='%.1f' y='%.1f' width='26' height='14' fill='#5dade2' stroke='%s' stroke-width='1'/>" % (cx - 13, b - 22, INK))
        s.append("<ellipse cx='%.1f' cy='%.1f' rx='13' ry='3' fill='#c3c7cb' stroke='%s' stroke-width='1.1'/>" % (cx, b - 30, INK))
    elif kind == "toy car":
        s.append("<path d='M%.1f %.1f h12 l6 -9 h18 l6 9 h6 v12 h-48 Z' fill='#e05a6a' stroke='%s' stroke-width='1.3' "
                 "stroke-linejoin='round'/>" % (cx - 24, b - 17, INK))
        s.append("<rect x='%.1f' y='%.1f' width='14' height='6' fill='#cfe3f7'/>" % (cx - 5, b - 24))
        for dx in (-13, 13):
            s.append("<circle cx='%.1f' cy='%.1f' r='6' fill='%s'/>" % (cx + dx, b - 6, INK))
    elif kind == "teddy":
        for dx in (-9, 9):
            s.append("<circle cx='%.1f' cy='%.1f' r='5' fill='#b07a4f' stroke='%s' stroke-width='1.2'/>" % (cx + dx, b - 43, INK))
        s.append("<circle cx='%.1f' cy='%.1f' r='15' fill='#b07a4f' stroke='%s' stroke-width='1.3'/>" % (cx, b - 15, INK))
        s.append("<circle cx='%.1f' cy='%.1f' r='11' fill='#b07a4f' stroke='%s' stroke-width='1.3'/>" % (cx, b - 37, INK))
        s.append("<circle cx='%.1f' cy='%.1f' r='1.6' fill='%s'/><circle cx='%.1f' cy='%.1f' r='1.6' fill='%s'/>"
                 % (cx - 4, b - 39, INK, cx + 4, b - 39, INK))
    elif kind == "shoe":
        s.append("<path d='M%.1f %.1f v-20 h14 q4 10 16 10 q10 0 12 10 Z' fill='#6d4c41' stroke='%s' stroke-width='1.3' "
                 "stroke-linejoin='round'/>" % (cx - 22, b, INK))
        s.append("<rect x='%.1f' y='%.1f' width='44' height='4' fill='%s'/>" % (cx - 22, b - 4, INK))
    elif kind == "egg":
        s.append("<ellipse cx='%.1f' cy='%.1f' rx='10' ry='13' fill='#fff8e7' stroke='%s' stroke-width='1.3'/>" % (cx, b - 13, INK))
    elif kind == "watermelon":
        s.append("<ellipse cx='%.1f' cy='%.1f' rx='30' ry='20' fill='#7fbf5f' stroke='%s' stroke-width='1.3'/>" % (cx, b - 20, INK))
        for dx in (-14, 0, 14):
            s.append("<path d='M%.1f %.1f Q%.1f %.1f %.1f %.1f' fill='none' stroke='#3f7d3a' stroke-width='1.4'/>"
                     % (cx + dx, b - 39, cx + dx * 1.4, b - 20, cx + dx, b - 1))
    elif kind == "cubes":
        per = 4
        for i in range(n):
            r, k = divmod(i, per)
            inrow = min(per, n - r * per)
            x = cx - inrow * SC / 2.0 + k * SC
            y = b - (r + 1) * SC
            s.append("<rect x='%.1f' y='%.1f' width='%d' height='%d' fill='%s' stroke='%s' stroke-width='1.1'/>"
                     % (x, y, SC, SC, CUBE_COLOURS[(r + k) % 2], INK))
    else:
        raise ValueError(kind)
    return "".join(s)


def balance_svg(left, right, tilt, labels=None):
    """left/right: (kind, n). tilt: 'L' (left side down), 'R' (right side down) or '=' (level)."""
    W, cx, py, half, d = 280, 140, 84, 80, 16
    dl = {"L": d, "R": -d, "=": 0}[tilt]
    yl, yr = py + dl, py - dl
    s = []
    s.append("<path d='M%d %d L%d %d L%d %d Z' fill='#c9ced3' stroke='%s' stroke-width='1.5' stroke-linejoin='round'/>"
             % (cx, py, cx - 24, py + 52, cx + 24, py + 52, INK))
    s.append("<rect x='%d' y='%d' width='80' height='6' rx='2' fill='#8a8f94' stroke='%s' stroke-width='1.2'/>" % (cx - 40, py + 52, INK))
    s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='6' stroke-linecap='round'/>"
             % (cx - half, yl, cx + half, yr, GREEN))
    s.append("<circle cx='%d' cy='%d' r='5' fill='%s'/>" % (cx, py, INK))
    names = []
    for (kind, n), x, y in [(left, cx - half, yl), (right, cx + half, yr)]:
        top = y - 10
        s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='3'/>" % (x, y, x, top, INK))
        s.append("<path d='M%d %d h80 l-6 5 h-68 Z' fill='#d8dde2' stroke='%s' stroke-width='1.3' stroke-linejoin='round'/>"
                 % (x - 40, top - 1, INK))
        s.append(thing(kind, x, top - 1, n))
        names.append("%d cubes" % n if kind == "cubes" else kind)
    if labels is None:
        labels = names
    for lab, x in zip(labels, (cx - half, cx + half)):
        if lab:
            s.append(text(x, py + 78, lab, 15))
    word = {"L": "the left side is down", "R": "the right side is down", "=": "the two sides are level"}[tilt]
    return svg_wrap(W, py + 86, "".join(s), "balance scale with %s on the left and %s on the right, %s" % (names[0], names[1], word), lg=True)


# ------------------------------------------------------------ containers
def container(x, b, w, h, frac, full_cup=False):
    """Straight-sided container from x to x+w, bottom at b, height h. Water fills frac of the height exactly."""
    s = []
    if frac > 0:
        wh = h * frac
        s.append("<rect x='%.1f' y='%.1f' width='%.1f' height='%.1f' fill='%s'/>" % (x, b - wh, w, wh, WATER))
        s.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='2'/>" % (x, b - wh, x + w, b - wh, WATER_LINE))
    s.append("<path d='M%.1f %.1f L%.1f %.1f L%.1f %.1f L%.1f %.1f' fill='none' stroke='%s' stroke-width='3' stroke-linejoin='round'/>"
             % (x, b - h - 2, x, b, x + w, b, x + w, b - h - 2, INK))
    return "".join(s)


LEVEL = {"full": 1.0, "nearly full": 0.85, "half full": 0.5, "quarter full": 0.25, "nearly empty": 0.08, "empty": 0.0}


def glass_svg(state, kind="glass"):
    w, h = (44, 84) if kind == "glass" else (74, 66)
    W = w + 40
    H = h + 16
    body = container(20, h + 10, w, h, LEVEL[state])
    return svg_wrap(W, H, body, "%s that is %s" % (kind, state))


def glasses_svg(states, labels="ABCD"):
    w, h, gap = 44, 84, 30
    s = []
    for i, st in enumerate(states):
        x = 16 + i * (w + gap)
        s.append(container(x, h + 10, w, h, LEVEL[st]))
        s.append(text(x + w / 2.0, h + 32, labels[i] if isinstance(labels, str) else labels[i], 18 if isinstance(labels, str) else 14))
    W = 32 + len(states) * w + (len(states) - 1) * gap
    desc = ", ".join("%s %s" % (labels[i], st) for i, st in enumerate(states))
    return svg_wrap(W, h + 40, "".join(s), "glasses of the same size: " + desc, lg=True)


def sizes_svg(sizes):
    """Full containers of different sizes, labelled A-D. sizes: list of (w, h)."""
    gap = 22
    maxh = max(h for _, h in sizes)
    b = maxh + 10
    s = []
    x = 16
    for i, (w, h) in enumerate(sizes):
        s.append(container(x, b, w, h, 1.0))
        s.append(text(x + w / 2.0, b + 22, "ABCD"[i], 18))
        x += w + gap
    desc = ", ".join("%s %d wide %d high" % ("ABCD"[i], w, h) for i, (w, h) in enumerate(sizes))
    return svg_wrap(int(x - gap + 16), b + 30, "".join(s), "full containers of different sizes: " + desc, lg=True)


def cups_jug_svg(n):
    """An empty jug and n full cups (rows of up to 5)."""
    jw, jh = 64, 96
    b = jh + 10
    s = [container(16, b, jw, jh, 0.0)]
    s.append("<path d='M%d %d C%d %d %d %d %d %d' fill='none' stroke='%s' stroke-width='3'/>"
             % (16 + jw, b - jh + 20, 16 + jw + 20, b - jh + 20, 16 + jw + 20, b - 40, 16 + jw, b - 40, INK))
    s.append(text(16 + jw / 2.0, b + 22, "jug", 15))
    cw, ch = 24, 30
    x0 = 16 + jw + 44
    rows = [min(5, n - r * 5) for r in range((n + 4) // 5)]
    for r, k in enumerate(rows):
        for i in range(k):
            s.append(container(x0 + i * (cw + 10), b - r * (ch + 14), cw, ch, 0.8))
    W = x0 + 5 * (cw + 10) - 10 + 16 if n >= 5 else x0 + n * (cw + 10) - 10 + 16
    return svg_wrap(W, b + 30, "".join(s), "an empty jug and %d cups of water" % n, lg=True)



def mixed_svg(kind, units):
    """The object is measured with a row that mixes cubes and paper clips (end to end, no gaps)."""
    L = sum(PU[x] for x in units)
    x0, x1 = PADL, PADL + L
    y = 6
    s = [guide(x0, y - 3, y + 2 * BAND + 8), guide(x1, y - 3, y + 2 * BAND + 8), draw_object(kind, x0, x1, y, y + BAND)]
    x = x0
    for i, un in enumerate(units):
        if un == "cube":
            s.append(cube(x, y + BAND + 6, i))
        else:
            s.append(draw_object("paper clip", x, x + PU["clip"], y + BAND + 6, y + 2 * BAND + 6))
        x += PU[un]
    assert x == x1
    return svg_wrap(int(x1 + PADL), int(y + 2 * BAND + 12), "".join(s),
                    "%s measured with: mixed" % kind, lg=True)


# ------------------------------------------------------------ area: shapes made of squares and sticky notes
SQ = 22


def shape_cells(name):
    w, h = name
    return [(c, r) for r in range(h) for c in range(w)]


def grid_shapes_svg(shapes):
    """shapes: list of cell lists [(col, row)]. Each square is SQ wide. Shapes sit on one line, labelled A, B, C."""
    gap = 34
    x = 16
    hmax = max(max(r for _, r in cells) + 1 for cells in shapes)
    base = 8 + hmax * SQ
    s = []
    desc = []
    for i, cells in enumerate(shapes):
        w = max(c for c, _ in cells) + 1
        h = max(r for _, r in cells) + 1
        top = base - h * SQ
        for c, r in cells:
            s.append("<rect x='%d' y='%d' width='%d' height='%d' fill='%s' stroke='%s' stroke-width='1.3'/>"
                     % (x + c * SQ, top + r * SQ, SQ, SQ, ["#9cc3ee", "#f7c873", "#b5d55a"][i % 3], INK))
        if len(shapes) > 1:
            s.append(text(x + w * SQ / 2.0, base + 22, "ABC"[i], 17))
        desc.append("%s%d squares" % ("" if len(shapes) == 1 else "ABC"[i] + " ", len(cells)))
        x += w * SQ + gap
    W = x - gap + 16
    H = base + (30 if len(shapes) > 1 else 8)
    return svg_wrap(W, H, "".join(s), "shapes made of squares: " + ", ".join(desc), lg=W > 200)


def notes_svg(cols, rows):
    """A placemat covered exactly by cols x rows sticky notes."""
    S = 26
    x0, y0 = 14, 10
    s = ["<rect x='%d' y='%d' width='%d' height='%d' fill='#e05a6a' stroke='%s' stroke-width='3'/>"
         % (x0 - 6, y0 - 6, cols * S + 12, rows * S + 12, INK)]
    for r in range(rows):
        for c in range(cols):
            s.append("<rect x='%d' y='%d' width='%d' height='%d' fill='#f9e27a' stroke='%s' stroke-width='1.2'/>"
                     % (x0 + c * S, y0 + r * S, S, S, INK))
    return svg_wrap(cols * S + 28, rows * S + 26, "".join(s),
                    "a placemat covered by %d sticky notes, %d across and %d down" % (cols * rows, cols, rows))


L5 = [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0)]
T7 = [(0, 0), (1, 0), (2, 0), (0, 1), (1, 1), (2, 1), (1, 2)]
L6 = [(0, 0), (0, 1), (0, 2), (1, 2), (2, 2), (3, 2)]


# ============================================================ set 1: longer, shorter, taller
def set_compare(P):
    its = []
    OTHER = ["They are the same.", "You cannot tell."]

    def two(objs, ask, picture, up=False):
        (a, la), (b, lb) = objs
        names = [the(a), the(b)]
        if la == lb:
            if up:
                e = "Both stand on the same floor. The tops are at the same height. They are <b>the same height</b>."
            else:
                e = "Both start at the same line. Both end at the same place. They are <b>the same length</b>."
            return mcq(fig(picture) + "Which is %s?" % ask, "They are the same.", names + ["You cannot tell."], e)
        big, small = (a, b) if la > lb else (b, a)
        win = big if ask in ("longer", "taller") else small
        lose = small if win == big else big
        if not up:
            e = ("Both start at the same line. Look at the other end. The %s goes further, so it is longer. "
                 "The <b>%s is %s</b>." % (big, win, ask))
        else:
            e = ("Both stand on the same floor. Look at the tops. The %s reaches higher, so it is taller. "
                 "The <b>%s is %s</b>." % (big, win, ask))
        return mcq(fig(picture) + "Which is %s?" % ask, the(win), [the(lose)] + OTHER, e)

    for objs, ask in [((("pencil", 9), ("crayon", 5)), "longer"), ((("ribbon", 6), ("straw", 10)), "longer"),
                      ((("nail", 5), ("pencil", 8)), "shorter"), ((("key", 3), ("marker", 7)), "longer")]:
        its.append(two(objs, ask, compare_svg([(k, 0, L) for k, L in objs])))
    its.append(two((("crayon", 6), ("key", 6)), "longer", compare_svg([("crayon", 0, 6), ("key", 0, 6)])))
    for objs, ask in [((("strip of paper", 11), ("crayon", 6)), "shorter"), ((("eraser", 3), ("ribbon", 7)), "shorter"),
                      ((("craft stick", 8), ("leaf", 4)), "longer"), ((("worm", 5), ("caterpillar", 8)), "shorter")]:
        its.append(two(objs, ask, compare_svg([(k, 0, L) for k, L in objs])))

    for objs, ask in [((("pencil", 8), ("crayon", 5)), "taller"), ((("marker", 6), ("straw", 9)), "taller"),
                      ((("craft stick", 7), ("crayon", 4)), "shorter"), ((("straw", 8), ("pencil", 8)), "taller")]:
        its.append(two(objs, ask, tall_svg(list(objs)), up=True))

    for (a, la), (b, sb, lb) in [(("pencil", 7), ("crayon", 4, 5)), (("ribbon", 8), ("straw", 5, 6)),
                                 (("marker", 7), ("craft stick", 5, 4))]:
        assert la > lb and sb + lb > la
        q = fig(compare_svg([(a, 0, la), (b, sb, lb)], line=False)) + "The ends are not lined up. Which is longer?"
        e = ("The %s ends further along, but it starts later. Slide it back so the ends line up. "
             "Then the %s sticks out past it. The <b>%s is longer</b>." % (b, a, a))
        its.append(mcq(q, the(a), [the(b)] + OTHER, e))

    its.append(mcq("You want to find the longer pencil. What do you do first?", "Line up the ends.",
                   ["Look at the colours.", "Count the pencils.", "Look at the tips only."],
                   "Put the pencils side by side. <b>Line up one end</b>. Then look at the other end. "
                   "The one that sticks out is longer."))
    its.append(mcq("A hockey stick is longer than a ruler. Which is true?", "The ruler is shorter.",
                   ["The ruler is longer.", "The hockey stick is shorter.", "They are the same."],
                   "The hockey stick is longer than the ruler. So the ruler is <b>shorter</b> than the hockey stick. "
                   "It is the same fact said the other way."))
    a = P.next()
    m = P.next()
    its.append(mcq("%s and %s stand back to back. %s’s head is higher. Who is taller?" % (a[0], m[0], a[0]), a[0],
                   [m[0], "They are the same.", "You cannot tell."],
                   "Their feet are on the same floor. The higher head belongs to the taller child. "
                   "<b>%s is taller</b>." % a[0]))
    a = P.next()
    m = P.next()
    its.append(mcq("%s’s scarf is shorter than %s’s scarf. Which is true?" % (a[0], m[0]),
                   "%s’s is longer." % m[0],
                   ["%s’s is longer." % a[0], "They are the same.", "%s’s is shorter." % m[0]],
                   "If %s’s scarf is shorter, then %s’s scarf is longer. <b>%s’s is longer</b>." % (a[0], m[0], m[0])))
    assert len(its) == 20, len(its)
    return {"title": "Longer, shorter and taller", "items": its}


# ============================================================ set 2: measure with cubes and paper clips
S2 = [("crayon", 4, "cube", None), ("key", 3, "cube", None), ("pencil", 7, "cube", None),
      ("eraser", 2, "clip", None), ("ribbon", 5, "cube", None), ("leaf", 3, "clip", None),
      ("straw", 9, "cube", None), ("marker", 4, "clip", None), ("caterpillar", 6, "cube", None),
      ("strip of paper", 5, "clip", None), ("nail", 5, "cube", 8), ("craft stick", 4, "clip", 6)]

OK = "Yes, it is right."
GAP = "No, there are gaps."
OVER = "No, they overlap."
START = "No, the start is wrong."
MIXED = "No, the units are mixed."
MODE_ANS = {"exact": OK, "gap": GAP, "overlap": OVER, "late": START, "mixed": MIXED}


def set_units(P):
    its = []
    asks = ["How many %s long is the %s?", "Count the %s. How long is the %s?"]
    for i, (kind, L, unit, total) in enumerate(S2):
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
            e += " Count the %s, not the lines between them. Touch each one as you count." % un
            cands = [L - 1, L + 1, L + 2]
        its.append(mcq_len(q, L, unit, cands, e))

    for kind, L, unit, mode in [("pencil", 7, "cube", "exact"), ("crayon", 4, "clip", "gap"),
                                ("ribbon", 7, "clip", "overlap"), ("straw", 6, "cube", "late"),
                                ("pencil", 6, None, "mixed")]:
        if mode == "mixed":
            units = ["clip", "clip", "cube", "cube"]
            assert sum(PU[x] for x in units) == L * PX
            q = fig(mixed_svg(kind, units)) + "Is this the right way to measure the %s?" % kind
            e = ("<b>No, the units are mixed.</b> Some are cubes and some are paper clips. "
                 "A paper clip is longer than a cube, so the count means nothing. Use only one kind of unit.")
        else:
            q = fig(wrong_svg(kind, L, unit, mode)) + "Is this the right way to measure the %s?" % kind
            un = UNAME[unit][1]
            if mode == "exact":
                e = ("Yes. The %s start at one end of the %s and go to the other end. They touch with no gaps. "
                     "They are all the same. The %s is <b>%s</b> long." % (un, kind, kind, u(L, unit)))
            elif mode == "gap":
                e = ("<b>No, there are gaps</b> between the %s. The gaps are not counted, so the number is too small. "
                     "Push the %s together so they touch." % (un, un))
            elif mode == "overlap":
                e = "<b>No, the %s overlap</b>. Some lie on top of others, so you count too many. Lay them end to end." % un
            else:
                e = ("<b>No, the start is wrong.</b> The first %s does not start at the end of the %s. "
                     "Line up the first one with the end of the %s." % (UNAME[unit][0], kind, kind))
        right = MODE_ANS[mode]
        others = [x for x in [OK, GAP, OVER, START, MIXED] if x != right]
        if mode in ("gap", "overlap", "late"):
            others = [x for x in others if x != MIXED]
        elif mode == "exact":
            others = [x for x in others if x != MIXED]
        else:
            others = [x for x in others if x != START]
        its.append(mcq(q, right, others, e))

    nm, he, his = P.next()
    n = n_gap(6, "cube")
    q = fig(wrong_svg("pencil", 6, "cube", "gap")) + "%s left gaps between the cubes. %s counts %s. How long is the pencil really?" % (nm, cap(he), u(n, "cube"))
    its.append(mcq(q, "more than %d cubes" % n, ["fewer than %d cubes" % n, "exactly %d cubes" % n, "You cannot measure it."],
                   "The gaps are part of the pencil too, but nobody counted them. So the pencil is <b>more than %d cubes</b> long. "
                   "Push the cubes together and count again." % n))
    its.append(mcq("You measure a crayon with cubes. What do you count?", "the cubes under it",
                   ["all the cubes in the box", "the lines between cubes", "the colours of the cubes"],
                   "Lay cubes along the crayon from end to end. Count only <b>the cubes under the crayon</b>. "
                   "That number is its length."))
    its.append(mcq("Should the cubes touch when you measure?", "Yes, with no gaps.",
                   ["No, leave gaps.", "Only some of them.", "It does not matter."],
                   "Lay the cubes <b>end to end</b>. They must touch, with no gaps and no overlaps."))
    order = [0, 1, 2, 3, 18, 4, 5, 12, 6, 7, 19, 13, 8, 9, 14, 15, 10, 16, 11, 17]
    assert sorted(order) == list(range(20))
    its = [its[i] for i in order]
    assert len(its) == 20, len(its)
    return {"title": "Measure with cubes and paper clips", "items": its}


# ============================================================ set 3: heavier and lighter
SAME = "They weigh the same."
CANT = "You cannot tell."


def set_mass(P):
    its = []

    def pair(a, b, tilt, ask, trap=False):
        heavy, light = (a, b) if tilt == "L" else (b, a)
        win = heavy if ask == "heavier" else light
        lose = light if win == heavy else heavy
        q = fig(balance_svg((a, 0), (b, 0), tilt)) + "Which is %s?" % ask
        if ask == "heavier":
            e = "The heavier side goes down. The %s side is down, so the <b>%s is heavier</b>." % (heavy, heavy)
        else:
            e = ("The heavier side goes down and the lighter side goes up. The %s side is up, "
                 "so the <b>%s is lighter</b>." % (light, light))
        if trap:
            e += " The %s looks bigger, but bigger is not always heavier." % light
        return mcq(q, the(win), [the(lose), SAME, CANT], e)

    its.append(pair("book", "feather", "L", "heavier"))
    its.append(pair("orange", "watermelon", "R", "heavier"))
    its.append(pair("brick", "sponge", "L", "lighter"))
    its.append(pair("egg", "shoe", "R", "lighter"))
    its.append(mcq("On a balance, which side goes down?", "the heavier side",
                   ["the lighter side", "the bigger thing", "the left side"],
                   "The <b>heavier side</b> goes down. The lighter side goes up."))
    q = fig(balance_svg(("apple", 0), ("orange", 0), "=")) + "The scale is level. Which is true?"
    its.append(mcq(q, SAME, ["The apple is heavier.", "The orange is heavier.", CANT],
                   "The two sides are level. Neither side goes down. So <b>they weigh the same</b>."))
    its.append(pair("teddy", "brick", "R", "heavier"))
    its.append(pair("pear", "can of beans", "R", "lighter"))
    its.append(pair("beach ball", "stone", "R", "heavier", trap=True))
    its.append(pair("pillow", "can of beans", "R", "heavier", trap=True))
    its.append(mcq("Is a bigger thing always heavier?", "No. Check on a balance.",
                   ["Yes, always.", "Yes, if it is wider.", "Yes, if it is taller."],
                   "<b>No.</b> A big pillow is lighter than a small can of beans. Put them on a balance to find out."))
    for kind, n in [("apple", 6), ("toy car", 9), ("shoe", 8)]:
        q = fig(balance_svg((kind, 0), ("cubes", n), "=", labels=[kind, ""])) + "The scale is level. How many cubes balance the %s?" % kind
        e = ("The scale is level, so the cubes weigh the same as the %s. Count the cubes: %s. "
             "<b>%d cubes</b> balance the %s." % (kind, count_list(n), n, kind))
        its.append(mcq_len(q, n, "cube", [n + 1, n - 1, n + 2], e))
    q = fig(balance_svg(("orange", 0), ("cubes", 4), "L", labels=["orange", "4 cubes"])) + "Which is true?"
    its.append(mcq(q, "The orange is heavier than 4 cubes.",
                   ["The orange is lighter than 4 cubes.", "The orange weighs the same as 4 cubes.", CANT],
                   "The orange side goes down. The side that goes down is heavier. So <b>the orange is heavier than 4 cubes</b>."))
    q = fig(balance_svg(("egg", 0), ("cubes", 5), "R", labels=["egg", "5 cubes"])) + "Which is true?"
    its.append(mcq(q, "The egg is lighter than 5 cubes.",
                   ["The egg is heavier than 5 cubes.", "The egg weighs the same as 5 cubes.", CANT],
                   "The egg side goes up. The side that goes up is lighter. So <b>the egg is lighter than 5 cubes</b>."))
    nm, he, his = P.next()
    its.append(mcq("%s puts 5 cubes on one side. %s puts 3 cubes on the other side. Which side goes down?" % (nm, cap(he)),
                   "the side with 5 cubes", ["the side with 3 cubes", "Both sides stay level.", CANT],
                   "5 cubes are heavier than 3 cubes. The heavier side goes down: <b>the side with 5 cubes</b>."))
    its.append(mcq("A ball balances 7 cubes. A boot balances 9 cubes. Which is lighter?", "the ball",
                   ["the boot", SAME, CANT],
                   "7 cubes is less than 9 cubes. So <b>the ball</b> is lighter. The boot is heavier."))
    nm, he, his = P.next()
    its.append(mcq("%s holds a book in one hand and an apple in the other. The book pulls %s hand down more. Which is heavier?"
                   % (nm, his), "the book", ["the apple", SAME, CANT],
                   "The heavier thing pulls your hand down more. So <b>the book</b> is heavier."))
    its.append(mcq("An apple balances 6 cubes. An orange also balances 6 cubes. Which is true?", SAME,
                   ["The apple is heavier.", "The orange is heavier.", CANT],
                   "Both balance the same number of cubes. So <b>they weigh the same</b>."))
    assert len(its) == 20, len(its)
    return {"title": "Heavier and lighter on a balance", "items": its}


# ============================================================ set 4: holds more, holds less
def set_capacity(P):
    its = []
    ABCD = ["A", "B", "C", "D"]
    its.append(mcq(fig(glasses_svg(["nearly full", "half full", "quarter full", "empty"])) +
                   "The glasses are the same size. Which has the most water?", "A", ABCD,
                   "The glasses are the same size, so look for the highest water. Glass A is nearly full. <b>A</b> has the most.",
                   lock=True))
    its.append(mcq(fig(glasses_svg(["full", "half full", "quarter full", "nearly empty"])) +
                   "The glasses are the same size. Which has the least water?", "D", ABCD,
                   "Look for the lowest water. Glass D is nearly empty. So <b>D</b> has the least.", lock=True))
    its.append(mcq("Which can hold more water?", "a bathtub", ["a cup", "a spoon", "They hold the same."],
                   "A bathtub is much bigger inside than a cup or a spoon. <b>A bathtub</b> holds more."))
    its.append(mcq(fig(glasses_svg(["quarter full", "half full", "nearly full", "nearly empty"])) +
                   "The glasses are the same size. Which has the most water?", "C", ABCD,
                   "Look for the highest water. Glass C is nearly full. <b>C</b> has the most.", lock=True))
    its.append(mcq(fig(glasses_svg(["half full", "nearly empty", "full", "quarter full"])) +
                   "The glasses are the same size. Which has the least water?", "B", ABCD,
                   "Look for the lowest water. Glass B is nearly empty. It has less than D. So <b>B</b> has the least.", lock=True))
    its.append(mcq(fig(sizes_svg([(34, 60), (70, 90), (24, 90), (50, 40)])) +
                   "Each container is full. Which one holds the most?", "B", ABCD,
                   "B is the widest and as tall as C. C is tall but very thin. So <b>B</b> holds the most. "
                   "Tall does not always mean it holds more.", lock=True))
    its.append(mcq(fig(sizes_svg([(40, 70), (60, 50), (24, 30), (34, 90)])) +
                   "Each container is full. Which one holds the least?", "C", ABCD,
                   "C is the thinnest and the shortest. So <b>C</b> holds the least.", lock=True))
    its.append(mcq(fig(sizes_svg([(30, 60), (40, 50), (26, 80), (72, 88)])) +
                   "Each container is full. Which one holds the most?", "D", ABCD,
                   "D is the widest and the tallest. So <b>D</b> holds the most. C is tall, but it is thin.", lock=True))
    its.append(mcq(fig(sizes_svg([(20, 40), (56, 60), (40, 90), (46, 70)])) +
                   "Each container is full. Which one holds the least?", "A", ABCD,
                   "A is the thinnest and the shortest. So <b>A</b> holds the least.", lock=True))
    for n in (3, 5, 6):
        nm, he, his = P.next()
        q = fig(cups_jug_svg(n)) + "%s pours all the cups into the jug. Now the jug is full. How many cups does the jug hold?" % nm
        e = "Count the cups: %s. The jug holds <b>%d cups</b> of water. Do not count the jug." % (count_list(n), n)
        its.append(mcq(q, "%d cups" % n, ["%d cups" % (n + 1), "%d cups" % (n - 1), "%d cups" % (n + 2)], e))
    its.append(mcq("A pot holds 9 cups of water. A bowl holds 4 cups. Which holds more?", "the pot",
                   ["the bowl", "They hold the same.", CANT],
                   "9 cups is more than 4 cups. So <b>the pot</b> holds more."))
    its.append(mcq("A vase holds 7 cups of water. A kettle holds 10 cups. Which holds less?", "the vase",
                   ["the kettle", "They hold the same.", CANT],
                   "7 cups is less than 10 cups. So <b>the vase</b> holds less."))
    its.append(mcq("A jug holds 6 cups of water. A pot holds 6 cups too. Which holds more?", "They hold the same.",
                   ["the jug", "the pot", CANT],
                   "Both hold 6 cups. So <b>they hold the same</b>."))
    nm, he, his = P.next()
    its.append(mcq("%s fills a bottle with water. %s pours it all into an empty mug. The mug spills over. Which holds more?"
                   % (nm, cap(he)), "the bottle", ["the mug", "They hold the same.", CANT],
                   "The water did not all fit in the mug. So <b>the bottle</b> holds more than the mug."))
    nm, he, his = P.next()
    its.append(mcq("%s pours a full glass into an empty bowl. The bowl is not full yet. Which holds more?" % nm,
                   "the bowl", ["the glass", "They hold the same.", CANT],
                   "All the water fit, and there is still room. So <b>the bowl</b> holds more than the glass."))
    its.append(mcq("You fill two jugs with cups of water to compare them. Which cup do you use?", "the same cup each time",
                   ["a big cup, then a small cup", "any cup at all", "a different cup for each jug"],
                   "Use <b>the same cup each time</b>. Then the counts can be compared. Different cups give counts that do not match."))
    a, b = P.next(), P.next()
    its.append(mcq("%s fills a pail with a small cup. %s fills the same pail with a big jug. Who pours more times?"
                   % (a[0], b[0]), a[0], [b[0], "They pour the same.", CANT],
                   "A small cup holds less each time, so it takes more pours. <b>%s</b> pours more times." % a[0]))
    its.append(mcq("You pour all the water from a tall thin glass into a wide bowl. Is there more water now?", "No, the same amount.",
                   ["Yes, more water.", "No, less water.", "There is no water."],
                   "The water looks lower in the wide bowl, but none was added or spilled. There is <b>the same amount</b> of water."))
    assert len(its) == 20, len(its)
    return {"title": "Holds more and holds less", "items": its}


# ============================================================ set 5: covers more, order three things, word problems
def diff_e(a, b, d):
    e = "Take away the smaller number from the bigger one: %d − %d = <b>%d</b>. " % (a, b, d)
    if 2 <= d <= 5:
        e += "Or count on from %d to %d: %s. That is %d more. " % (b, a, count_list(d, b + 1), d)
    e += "Do not add: %d + %d = %d is both together." % (a, b, a + b)
    return e


def set_problems(P):
    its = []
    SH = ["shape A", "shape B", "They cover the same.", CANT]

    def covers(shapes, ask, ans, e):
        q = fig(grid_shapes_svg(shapes)) + "Which shape covers %s?" % ask
        return mcq(q, ans, SH, e, lock=True)

    its.append(covers([shape_cells((3, 2)), shape_cells((2, 2))], "more", "shape A",
                      "Count the squares. Shape A has 6. Shape B has 4. 6 is more, so <b>shape A</b> covers more."))
    q = fig(grid_shapes_svg([L6])) + "How many squares cover this shape?"
    its.append(mcq(q, "6 squares", ["5 squares", "7 squares", "8 squares"],
                   "Touch each square once as you count: 1, 2, 3, 4, 5, 6. <b>6 squares</b> cover the shape. "
                   "Do not count the corner square twice."))
    its.append(covers([shape_cells((4, 2)), shape_cells((3, 3))], "more", "shape B",
                      "Shape A is longer, but count the squares. Shape A has 8. Shape B has 9. "
                      "So <b>shape B</b> covers more. Longer does not always mean it covers more."))
    its.append(covers([L5, T7], "less", "shape A",
                      "Shape A is long, but it has only 5 squares. Shape B has 7 squares. "
                      "5 is less than 7, so <b>shape A</b> covers less."))
    q = fig(notes_svg(4, 2)) + "How many sticky notes cover the placemat?"
    its.append(mcq(q, "8 sticky notes", ["6 sticky notes", "4 sticky notes", "9 sticky notes"],
                   "There are 2 rows of 4 notes. Count them all: 1, 2, 3, 4, 5, 6, 7, 8. <b>8 sticky notes</b> cover the placemat. "
                   "Do not count only the top row."))
    its.append(covers([shape_cells((6, 2)), shape_cells((4, 3))], "more", "They cover the same.",
                      "Count the squares. Shape A has 12. Shape B has 12. They look different, but <b>they cover the same</b>."))
    a, b = P.next(), P.next()
    its.append(mcq("%s covers %s book with 8 sticky notes. %s covers %s book with 10 of the same notes. Whose book covers more?"
                   % (a[0], a[2], b[0], b[2]), "%s’s book" % b[0], ["%s’s book" % a[0], "They cover the same.", CANT],
                   "10 notes is more than 8 notes. So <b>%s’s book</b> covers more." % b[0]))
    nm, he, his = P.next()
    its.append(mcq("%s says the longer shape always covers more. Is %s right?" % (nm, he), "No. Count the squares.",
                   ["Yes, always.", "Yes, if it is thin.", "Only for squares."],
                   "<b>No.</b> A long, thin shape can cover less than a short, wide one. Cover both with the same squares and count."))

    for objs, ask in [((("straw", 10), ("key", 3), ("pencil", 7)), "longest")]:
        lens = [L for _, L in objs]
        names = [k for k, _ in objs]
        best = names[lens.index(max(lens))]
        mid = sorted(objs, key=lambda t: t[1])[1][0]
        q = fig(compare_svg([(k, 0, L) for k, L in objs])) + "Which is the %s?" % ask
        e = ("All three start at the same line. Look at where each one ends. The <b>%s</b> is the %s. "
             "The %s is in the middle." % (best, ask, mid))
        its.append(mcq(q, the(best), [the(n) for n in names if n != best] + ["They are the same."], e))
    objs = [("marker", 6), ("strip of paper", 11), ("leaf", 4)]
    q = fig(compare_svg([(k, 0, L) for k, L in objs])) + "Put them in order from shortest to longest."
    its.append(mcq(q, "leaf, marker, strip of paper",
                   ["strip of paper, marker, leaf", "marker, leaf, strip of paper", "leaf, strip of paper, marker"],
                   "Shortest first. The leaf ends first, then the marker, then the strip of paper. "
                   "So: <b>leaf, marker, strip of paper</b>. Do not start with the longest."))
    objs = [("crayon", 4), ("straw", 9), ("pencil", 7)]
    q = fig(tall_svg(objs)) + "Which is the tallest?"
    its.append(mcq(q, "the straw", ["the crayon", "the pencil", "They are the same."],
                   "All three stand on the same floor. The straw reaches highest. <b>The straw</b> is the tallest. "
                   "The pencil is in the middle."))
    q = fig(grid_shapes_svg([shape_cells((3, 3)), shape_cells((5, 2)), shape_cells((4, 2))])) + "Which shape covers the most?"
    its.append(mcq(q, "shape B", ["shape A", "shape B", "shape C", "They cover the same."],
                   "Count the squares. A has 9. B has 10. C has 8. 10 is the most, so <b>shape B</b> covers the most.", lock=True))
    its.append(mcq("The book is heavier than the apple. The apple is heavier than the feather. "
                   "Order them from heaviest to lightest.", "book, apple, feather",
                   ["feather, apple, book", "apple, book, feather", "book, feather, apple"],
                   "The book is heavier than the apple, and the apple is heavier than the feather. "
                   "Heaviest first: <b>book, apple, feather</b>."))
    nm, he, his = P.next()
    its.append(mcq("At the cottage, %s fills 3 pails with cups of water. The red pail holds 9 cups. The blue pail holds 6 cups. "
                   "The yellow pail holds 11 cups. Which holds the least?" % nm, "the blue pail",
                   ["the yellow pail", "the red pail", "They hold the same."],
                   "6 is the smallest number. So <b>the blue pail</b> holds the least. The yellow pail holds the most."))

    q = fig(measure2_svg([("pencil", 9), ("crayon", 5)], "cube")) + "How many cubes longer is the pencil than the crayon?"
    its.append(mcq_len(q, 4, "cube", [14, 5, 3, 9], "The pencil is 9 cubes long. The crayon is 5 cubes long. " + diff_e(9, 5, 4)))
    a, b = P.next(), P.next()
    its.append(mcq("At recess, %s builds a tower 9 blocks tall. %s’s tower is 4 blocks taller. How tall is %s’s tower?"
                   % (a[0], b[0], b[0]), "13 blocks", ["5 blocks", "9 blocks", "12 blocks"],
                   "“4 blocks taller” means add 4. 9 + 4 = <b>13</b>. It is taller, so the number must be bigger than 9."))
    its.append(mcq_len("A toy beaver balances 7 cubes. A toy moose balances 12 cubes. How many cubes heavier is the moose?",
                       5, "cube", [19, 6, 4], diff_e(12, 7, 5)))
    nm, he, his = P.next()
    its.append(mcq("At the cottage, a pail holds 9 cups of lake water. %s pours out 3 cups. How many cups are left?" % nm,
                   "6 cups", ["12 cups", "5 cups", "7 cups"],
                   "Pouring out means take away. 9 − 3 = <b>6</b>. There are 6 cups left. Do not add: 9 + 3 = 12."))
    nm, he, his = P.next()
    its.append(mcq_len("%s needs 12 cubes to balance %s lunch box. %s has put 9 cubes on the scale. How many more cubes does %s need?"
                       % (nm, his, cap(he), he), 3, "cube", [21, 2, 4],
                       "Count on from 9 to 12: 10, 11, 12. That is 3. Or 12 − 9 = <b>3</b>. Check: 9 + 3 = 12."))
    its.append(mcq("A bottle holds 5 cups of water. A jug holds 7 cups. How many cups do they hold together?", "12 cups",
                   ["2 cups", "11 cups", "13 cups"],
                   "Together means add. 5 + 7 = <b>12</b>. They hold 12 cups. Do not take away: 7 − 5 = 2 is the difference."))
    assert len(its) == 20, len(its)
    return {"title": "Covers more, ordering and word problems", "items": its}


# ============================================================ lesson
def body_html():
    return (
        "<h2>Longer, shorter and taller</h2>"
        "<p>Put two things side by side. Line up one end. Look at the other end. "
        "The one that sticks out is <b>longer</b>. The other is <b>shorter</b>. "
        "For things that stand up, we say <b>taller</b> and <b>shorter</b>.</p>"
        "<figure class='sn-fig'>" + compare_svg([("pencil", 0, 8), ("crayon", 0, 5)]) +
        "<figcaption>Both start at the same line. The pencil is longer. The crayon is shorter.</figcaption></figure>"
        "<h2>Measure with cubes or paper clips</h2>"
        "<p>Lay cubes along the object, <b>end to end</b>. Start right at one end. Stop at the other end. "
        "Count the cubes. That number is the length. Say the unit too: “6 cubes long”.</p>"
        "<figure class='sn-fig'>" + measure_svg("crayon", 6, "cube") +
        "<figcaption>6 cubes fit from one end of the crayon to the other. The crayon is 6 cubes long.</figcaption></figure>"
        "<p>Three rules: <b>no gaps</b>, <b>no overlaps</b> and <b>all the units the same</b>.</p>"
        "<figure class='sn-fig'>" + wrong_svg("crayon", 4, "clip", "gap") +
        "<figcaption>Wrong: there are gaps. Only 3 paper clips are counted, but the crayon is 4 paper clips long.</figcaption></figure>"
        "<h2>Heavier and lighter</h2>"
        "<p>Put two things on a balance. The <b>heavier</b> side goes down. The <b>lighter</b> side goes up. "
        "If the sides are level, they weigh the same.</p>"
        "<figure class='sn-fig'>" + balance_svg(("beach ball", 0), ("stone", 0), "R") +
        "<figcaption>The stone side is down, so the stone is heavier. The beach ball is bigger, but it is lighter.</figcaption></figure>"
        "<h2>Holds more and holds less</h2>"
        "<p>Fill a jug with cups of water. Use the same cup each time. Count the cups. "
        "A container that takes more cups <b>holds more</b>.</p>"
        "<figure class='sn-fig'>" + cups_jug_svg(4) +
        "<figcaption>4 cups of water fill the jug. The jug holds 4 cups.</figcaption></figure>"
        "<h2>Covers more</h2>"
        "<p>Cover each shape with squares that are all the same. Count the squares. "
        "The shape with more squares <b>covers more</b>.</p>"
        "<figure class='sn-fig'>" + grid_shapes_svg([shape_cells((4, 2)), shape_cells((3, 3))]) +
        "<figcaption>Shape A is longer, but it has 8 squares. Shape B has 9 squares, so shape B covers more.</figcaption></figure>"
        + ex("Order three things", "A straw is 10 cubes long. A key is 3 cubes long. A pencil is 7 cubes long. "
             "Order them from shortest to longest.", "Find the smallest number first: 3, then 7, then 10.",
             "key, pencil, straw")
        + ex("How many longer?", "A pencil is 9 cubes long. A crayon is 5 cubes long. How many cubes longer is the pencil?",
             "9 − 5 = 4. Or count on from 5: 6, 7, 8, 9. That is 4.", "4 cubes")
        + "<h2>Common mistakes</h2>"
        + table(["Mistake", "What to do instead"], [
            ["Not lining up the ends", "Start both objects at the same line"],
            ["Starting the cubes past the end", "Put the first cube right at one end"],
            ["Leaving gaps between cubes", "Push the cubes together so they touch"],
            ["Mixing cubes and paper clips", "Use one kind of unit all the way"],
            ["Thinking bigger means heavier", "Use a balance: the side that goes down is heavier"],
            ["Thinking longer covers more", "Cover both shapes with squares and count"],
        ])
    )


FAQ = [
    {"q": "What measurement do Grade 1 students learn in Ontario math?",
     "a": "In the Spatial Sense strand, Grade 1 students learn what can be measured (length, area, mass and capacity) "
          "and compare and order everyday objects by these attributes. They also measure length with non-standard units "
          "such as cubes and paper clips."},
    {"q": "What are non-standard units of measurement?",
     "a": "Non-standard units are everyday objects of the same size used to measure, like linking cubes, paper clips, "
          "craft sticks or cups. They show children that a length is how many equal units fit along an object, before they use rulers."},
    {"q": "Why must the units touch and be the same size?",
     "a": "Gaps and overlaps make the count too small or too big, and units of different sizes make the count meaningless. "
          "That is why two people using their own hand spans can get different answers, while two people using the same cubes agree."},
    {"q": "How can I practise measuring with my Grade 1 child at home?",
     "a": "Measure a book or a winter boot with LEGO bricks laid end to end, cover a placemat with sticky notes, "
          "count cups of water to fill two containers, and compare two things on a coat hanger balance."},
]


def gen():
    rnd = random.Random(41813)
    P = People(rnd)
    sets = [set_compare(P), set_units(P), set_mass(P), set_capacity(P), set_problems(P)]
    balance(sets, rnd)
    seen = set()
    for s in sets:
        assert len(s["items"]) == 20, (s["title"], len(s["items"]))
        assert sorted(it["a"] for it in s["items"]) == sorted([0, 1, 2, 3] * 5), s["title"]
        for it in s["items"]:
            assert len(set(it["c"])) == 4, it
            assert it["q"].count("<svg") <= 1
            k = it["q"]
            assert k not in seen, it["q"]
            seen.add(k)
            for c in it["c"]:
                assert not re.search(r"\b1 (cubes|paper clips|cups|sticks|blocks|squares)\b", c), c
                assert not re.search(r"\b([02-9]|\d\d+) (cube|paper clip|cup|stick|block|square)\b", c), c
    n = 0
    for s in sets:
        for it in s["items"]:
            ans = it["c"][it["a"]]
            m = re.search(r"aria-label='([a-z -]+) (\d+) (cubes|paper clips) long, above (\d+)", it["q"])
            if m:
                unit = "cube" if m.group(3) == "cubes" else "clip"
                assert ans == u(int(m.group(2)), unit)
                n += 1
            m = re.search(r"aria-label='balance scale with ([a-z ]+) on the left and (\d+) cubes on the right, the two sides are level", it["q"])
            if m:
                assert ans == "%s cubes" % m.group(2)
                n += 1
            m = re.search(r"aria-label='an empty jug and (\d+) cups", it["q"])
            if m:
                assert ans == "%s cups" % m.group(1)
                n += 1
            m = re.search(r"measured with ?(?:cubes|paper clips)?: (exact|gap|overlap|late|mixed)'", it["q"])
            if m and "Is this the right way" in it["q"]:
                assert ans == MODE_ANS[m.group(1)], it["q"]
                n += 1
            m = re.search(r"aria-label='shapes made of squares: ([^']+)'", it["q"])
            if m:
                cnt = [int(x) for x in re.findall(r"(\d+) squares", m.group(1))]
                if len(cnt) == 1:
                    assert ans == "%d squares" % cnt[0]
                else:
                    f = max if "more" in it["q"] or "most" in it["q"] else min
                    if cnt.count(f(cnt)) > 1:
                        assert ans == "They cover the same." and len(set(cnt)) == 1
                    else:
                        assert ans == "shape " + "ABC"[cnt.index(f(cnt))]
                n += 1
            m = re.search(r"aria-label='a placemat covered by (\d+) sticky notes", it["q"])
            if m:
                assert ans == "%s sticky notes" % m.group(1)
                n += 1
    assert n == 12 + 3 + 3 + 5 + 6 + 1, n
    for it in sets[2]["items"]:
        m = re.search(r"with ([a-z ]+) on the left and ([a-z ]+) on the right, the (left|right) side is down'", it["q"])
        if m and "Which is heavier" in it["q"]:
            assert it["c"][it["a"]] == "the " + (m.group(1) if m.group(3) == "left" else m.group(2))
        if m and "Which is lighter" in it["q"]:
            assert it["c"][it["a"]] == "the " + (m.group(2) if m.group(3) == "left" else m.group(1))
    for it in sets[3]["items"]:
        m = re.search(r"glasses of the same size: ([^']+)'", it["q"])
        if m:
            st = dict(x.split(" ", 1) for x in m.group(1).split(", "))
            ans = "ABCD"[it["a"]]
            f = max if "most" in it["q"] else min
            lv = [LEVEL[v] for v in st.values()]
            assert LEVEL[st[ans]] == f(lv) and lv.count(f(lv)) == 1
        m = re.search(r"full containers of different sizes: ([^']+)'", it["q"])
        if m:
            dims = [tuple(map(int, re.findall(r"\d+", x))) for x in m.group(1).split(", ")]
            areas = [w * h for w, h in dims]
            i = it["a"]
            f = max if "most" in it["q"] else min
            assert areas[i] == f(areas) and areas.count(f(areas)) == 1
            assert dims[i][0] == f(d[0] for d in dims) and dims[i][1] == f(d[1] for d in dims)
    return {
        "country": "ca-on", "subject": "math", "grade": "grade-1", "slug": "comparing-length-mass-and-capacity", "sort": 13,
        "updated": UPDATED, "pdf_url": "",
        "title": "Comparing Length, Mass and Capacity",
        "seo_title": "Grade 1 Comparing Length, Mass and Capacity Worksheets (Free, with Answer Key) | Ontario Math",
        "short_title": "Comparing length, mass and capacity",
        "domain": "Spatial Sense",
        "standard_code": "Grade 1: E2.2",
        "standard_url": "https://www.dcp.edu.gov.on.ca/en/curriculum/elementary-mathematics",
        "standard_text": "Compare several everyday objects and order them according to length, area, mass, and capacity",
        "meta_desc": "Free Grade 1 math worksheets on comparing length, mass and capacity: longer, shorter and taller, "
                     "measuring with cubes and paper clips with no gaps, heavier and lighter on a balance, which holds more, "
                     "which covers more, and ordering three objects. 100 picture questions with an answer key, "
                     "matched to the Ontario curriculum.",
        "key_big": "Line up the ends. Lay units end to end: no gaps, no overlaps, all the same.",
        "key_sub": "Count the units from one end to the other and say the unit: “6 cubes long”. "
                   "On a balance the heavier side goes down. Bigger is not always heavier.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }


if __name__ == "__main__":
    out = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, out["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(out, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
