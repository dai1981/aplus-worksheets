# -*- coding: utf-8 -*-
"""
CA-BC Grade 1 Math: Measuring with non-standard units (BC Mathematics Curriculum, Geometry and measurement:
direct measurement with non-standard units, non-uniform and uniform)
  python3 tools/gen_cabc_math_g1_measuring.py
Longer, shorter and taller with the ends lined up; measuring length with cubes and paper clips laid end to end
(no gaps, no overlaps); why same-size units matter; comparing and ordering three objects; heavier on a balance,
holds more, and BC word problems.
Every picture is drawn exactly from the data: objects run from one cube boundary to another, a paper clip is
exactly 2 cubes long, the heavier side of a balance is the lower one and water levels are exact.
Wrong answers come from real mistakes: not lining up the ends, gaps and overlaps, mixing units, comparing
counts made with different units, counting past the end and thinking bigger means heavier.
HTML attributes use single quotes (no backslashes in the JSON).
"""
import json, os, random, re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "ca-bc", "math", "grade-1")
UPDATED = "2026-11-02"
GREEN = "#006633"
INK = "#2b2b2b"
GREY = "#8a8a8a"
WATER = "#9fd3f2"
WATER_LINE = "#2a7fb8"
FONT = "Arial, Helvetica, sans-serif"
GIRLS = ["Olivia", "Ava", "Chloe", "Simran", "Jasleen", "Mei", "Hana", "Sofia", "Emma", "Leah", "Zara", "Nadia"]
BOYS = ["Liam", "Ethan", "Noah", "Arjun", "Harjot", "Wei", "Mateo", "Lucas", "Kai", "Owen", "Ryan"]

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




def unit_key_svg():
    """One paper clip above two cubes: a paper clip is exactly as long as 2 cubes."""
    x0 = PADL
    x1 = x0 + PU["clip"]
    s = [guide(x0, 3, 6 + 2 * BAND + 10), guide(x1, 3, 6 + 2 * BAND + 10),
         draw_object("paper clip", x0, x1, 6, 6 + BAND)]
    row, end = unit_row(x0, 6 + BAND + 6, 2, "cube")
    assert end == x1
    s.append(row)
    return svg_wrap(int(x1 + PADL), int(6 + 2 * BAND + 12), "".join(s), "1 paper clip is as long as 2 cubes")


def own_units_svg(objs):
    """objs: list of (kind, L, unit). Each object is measured with its own unit, one under the other."""
    s = []
    y = 6
    right = 0
    for kind, L, unit in objs:
        b, r, bt = measure_block(kind, L, unit, y)
        s.append(b)
        right = max(right, r)
        y = bt + 12
    desc = " and ".join("%s %d %s" % (k, L, UNAME[un][1]) for k, L, un in objs)
    return svg_wrap(int(right + PADL), int(y - 8), "".join(s), "measured with different units: " + desc, lg=True)


def towers_svg(heights):
    """Cube towers on one floor, labelled A, B, C."""
    C = 16
    gap = 30
    hmax = max(heights)
    base = 8 + hmax * C
    s = []
    x = 20
    for i, h in enumerate(heights):
        for k in range(h):
            s.append("<rect x='%d' y='%d' width='%d' height='%d' fill='%s' stroke='%s' stroke-width='1.1'/>"
                     % (x, base - (k + 1) * C, C * 2, C, CUBE_COLOURS[k % 2], INK))
        s.append(text(x + C, base + 22, "ABC"[i], 17))
        x += 2 * C + gap
    W = x - gap + 20
    s.append("<line x1='8' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='2.5'/>" % (base + 1, W - 8, base + 1, INK))
    desc = ", ".join("%s %d cubes" % ("ABC"[i], h) for i, h in enumerate(heights))
    return svg_wrap(W, base + 30, "".join(s), "cube towers: " + desc, lg=True)


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
            e = ("The ends are lined up. Look at the other end. The %s sticks out further. "
                 "The <b>%s is %s</b>." % (big, win, ask))
        else:
            e = ("Both stand on the same floor. Look at the tops. The %s reaches higher. "
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
                   "The hockey stick is longer than the ruler. So the ruler is <b>shorter</b>. "
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
                                ("ribbon", 7, "clip", "overlap"), ("straw", 6, "cube", "late")]:
        q = fig(wrong_svg(kind, L, unit, mode)) + "Is this the right way to measure the %s?" % kind
        un = UNAME[unit][1]
        if mode == "exact":
            e = ("Yes. The %s start at one end of the %s and stop at the other end. They touch with no gaps. "
                 "The %s is <b>%s</b> long." % (un, kind, kind, u(L, unit)))
        elif mode == "gap":
            e = ("<b>No, there are gaps</b> between the %s. Nobody counts the gaps, so the number is too small. "
                 "Push the %s together so they touch." % (un, un))
        elif mode == "overlap":
            e = "<b>No, the %s overlap</b>. Some lie on top of others, so you count too many. Lay them end to end." % un
        else:
            e = ("<b>No, the start is wrong.</b> The first %s does not start at the end of the %s. "
                 "Line up the first one with the end of the %s." % (UNAME[unit][0], kind, kind))
        right = MODE_ANS[mode]
        others = [x for x in [OK, GAP, OVER, START] if x != right]
        its.append(mcq(q, right, others, e))

    nm, he, his = P.next()
    n = n_gap(6, "cube")
    q = fig(wrong_svg("pencil", 6, "cube", "gap")) + "%s left gaps between the cubes. %s counts %s. How long is the pencil really?" % (nm, cap(he), u(n, "cube"))
    its.append(mcq(q, "more than %d cubes" % n, ["fewer than %d cubes" % n, "exactly %d cubes" % n, "You cannot measure it."],
                   "The gaps are part of the pencil too, but nobody counted them. So the pencil is <b>more than %d cubes</b> long. "
                   "Push the cubes together and count again." % n))
    nm, he, his = P.next()
    m = n_over(4, "clip")
    q = fig(wrong_svg("pencil", 4, "clip", "overlap")) + "%s’s paper clips overlap. %s counts %s. How long is the pencil really?" % (nm, cap(he), u(m, "clip"))
    its.append(mcq(q, "fewer than %d paper clips" % m,
                   ["more than %d paper clips" % m, "exactly %d paper clips" % m, "You cannot measure it."],
                   "The paper clips lie on top of each other, so %s counted too many. The pencil is "
                   "<b>fewer than %d paper clips</b> long. Lay them end to end and count again." % (he, m)))
    its.append(mcq("You measure a crayon with cubes. What do you count?", "the cubes under it",
                   ["all the cubes in the box", "the lines between cubes", "the colours of the cubes"],
                   "Lay cubes along the crayon from end to end. Count only <b>the cubes under the crayon</b>. "
                   "That number is its length."))
    its.append(mcq("Should the cubes touch when you measure?", "Yes, with no gaps.",
                   ["No, leave gaps.", "Only some of them.", "It does not matter."],
                   "Lay the cubes <b>end to end</b>. They must touch, with no gaps and no overlaps."))
    # 12 counts (0-11), 4 right-way (12-15), 4 more (16-19)
    order = [0, 1, 2, 3, 18, 4, 5, 12, 6, 7, 19, 13, 8, 9, 14, 15, 10, 16, 11, 17]
    assert sorted(order) == list(range(20))
    its = [its[i] for i in order]
    assert len(its) == 20, len(its)
    return {"title": "Measure with cubes and paper clips", "items": its}


# ============================================================ set 3: same-size units matter
def set_same_units(P):
    its = []
    # A paper clip is 2 cubes long: count both rows.
    for kind, cubes, ask in [("crayon", 4, "clip"), ("pencil", 8, "clip"), ("straw", 10, "cube"), ("ribbon", 6, "clip")]:
        clips = cubes // 2
        q = fig(two_units_svg(kind, cubes))
        if ask == "clip":
            q += "The %s is %s long. How many paper clips long is it?" % (kind, u(cubes, "cube"))
            e = ("Count the paper clips under the %s: %s. It is <b>%s</b> long. "
                 "A paper clip is longer than a cube, so you need fewer of them." % (kind, count_list(clips), u(clips, "clip")))
            its.append(mcq_len(q, clips, "clip", [cubes, clips + 1, clips - 1, clips + 2], e))
        else:
            q += "The %s is %s long. How many cubes long is it?" % (kind, u(clips, "clip"))
            e = ("Count the cubes under the %s: %s. It is <b>%s</b> long. "
                 "A cube is shorter than a paper clip, so you need more of them." % (kind, count_list(cubes), u(cubes, "cube")))
            its.append(mcq_len(q, cubes, "cube", [clips, cubes - 1, cubes + 1], e))
    q = fig(two_units_svg("marker", 6)) + "Why are there fewer paper clips than cubes?"
    its.append(mcq(q, "A paper clip is longer.", ["A paper clip is shorter.", "The marker got shorter.", "Someone counted wrong."],
                   "The marker is the same. <b>A paper clip is longer</b> than a cube, so fewer paper clips fit along it. "
                   "Bigger units give a smaller number."))
    q = fig(two_units_svg("pencil", 6)) + "Which unit fits more times along the pencil?"
    its.append(mcq(q, "cubes", ["paper clips", "They fit the same.", "You cannot tell."],
                   "6 cubes fit, but only 3 paper clips. <b>Cubes</b> fit more times because they are smaller."))
    q = fig(mixed_svg("pencil", ["clip", "clip", "cube", "cube"])) + "Is this the right way to measure the pencil?"
    its.append(mcq(q, MIXED, [OK, GAP, OVER],
                   "<b>No, the units are mixed.</b> Some are cubes and some are paper clips. "
                   "They are not the same size, so the count does not tell the length. Use one kind of unit."))
    nm, he, his = P.next()
    q = fig(mixed_svg("ribbon", ["cube", "clip", "cube", "clip"])) + "%s counts 4 and says the ribbon is 4 long. What is wrong?" % nm
    its.append(mcq(q, "The units are mixed.", ["There are gaps.", "They overlap.", "Nothing is wrong."],
                   "The units touch, but <b>the units are mixed</b>. 2 are cubes and 2 are paper clips. "
                   "With only cubes, the ribbon is 6 cubes long."))
    a, b = P.next(), P.next()
    q = (fig(own_units_svg([("ribbon", 6, "clip"), ("ribbon", 6, "cube")])) +
         "%s’s ribbon is on top: 6 paper clips. %s’s ribbon is below: 6 cubes. Whose ribbon is longer?" % (a[0], b[0]))
    its.append(mcq(q, "%s’s ribbon" % a[0], ["%s’s ribbon" % b[0], "They are the same.", "You cannot tell."],
                   "Both counts are 6, but the units are not the same. A paper clip is longer than a cube. "
                   "So <b>%s’s ribbon</b> is longer. You can only compare counts made with the same unit." % a[0]))
    a, b = P.next(), P.next()
    q = fig(unit_key_svg()) + "%s’s pencil is 5 paper clips long. %s’s pencil is 5 cubes long. Whose pencil is longer?" % (a[0], b[0])
    its.append(mcq(q, "%s’s pencil" % a[0], ["%s’s pencil" % b[0], "They are the same.", "You cannot tell."],
                   "1 paper clip is as long as 2 cubes. So 5 paper clips is longer than 5 cubes. "
                   "<b>%s’s pencil</b> is longer." % a[0]))
    q = fig(unit_key_svg()) + "A key is 2 paper clips long. How many cubes long is the key?"
    its.append(mcq_len(q, 4, "cube", [2, 3, 6],
                       "Each paper clip is as long as 2 cubes. 2 paper clips make 2 + 2 = <b>4 cubes</b>. "
                       "The key is 4 cubes long, not 2."))
    q = fig(unit_key_svg()) + "An eraser is 4 cubes long. How many paper clips long is it?"
    its.append(mcq_len(q, 2, "clip", [4, 8, 3],
                       "2 cubes make 1 paper clip. 4 cubes are 2 + 2, so the eraser is <b>2 paper clips</b> long."))
    nm, he, his = P.next()
    its.append(mcq("%s measures a desk with paper clips: 10 paper clips. Then %s measures it with cubes. What will %s get?"
                   % (nm, he, he), "more than 10 cubes", ["fewer than 10 cubes", "exactly 10 cubes", "You cannot measure it."],
                   "A cube is shorter than a paper clip. More cubes fit along the same desk. "
                   "So %s gets <b>more than 10 cubes</b>." % he))
    its.append(mcq("You measure one book with cubes and with paper clips. Which number is bigger?", "the number of cubes",
                   ["the number of clips", "They are the same.", "You cannot tell."],
                   "Cubes are smaller than paper clips. More cubes fit, so <b>the number of cubes</b> is bigger."))
    nm, he, his = P.next()
    its.append(mcq("%s measures a table: 9 hand spans. %s dad measures it: 6 hand spans. Why are the numbers different?"
                   % (nm, cap(his)), "Dad’s hands are bigger.",
                   ["%s’s hands are bigger." % nm, "The table got longer.", "Dad counted wrong."],
                   "It is the same table. <b>Dad’s hands are bigger</b>, so fewer of his hand spans fit. "
                   "Hands are not all the same size."))
    nm, he, his = P.next()
    its.append(mcq("%s crosses the rug in 8 steps. %s teacher crosses it in 5 steps. Which is true?" % (nm, cap(his)),
                   "The teacher’s steps are longer.",
                   ["%s’s steps are longer." % nm, "The rug is longer for %s." % nm, "Somebody counted wrong."],
                   "It is the same rug. The teacher needs fewer steps, so <b>the teacher’s steps are longer</b>."))
    its.append(mcq("You want to compare two desks. Which units should you use?", "the same units for both",
                   ["cubes, then paper clips", "any units at all", "a hand, then a foot"],
                   "Use <b>the same units for both</b> desks. Then the bigger number means the longer desk."))
    nm, he, his = P.next()
    its.append(mcq("%s measures with long sticks and short sticks mixed. Can %s trust the count?" % (nm, he),
                   "No, use one size.", ["Yes, it is fine.", "Yes, if they touch.", "Only if it is long."],
                   "<b>No.</b> The sticks are not the same size, so the number does not tell the length. "
                   "Use sticks that are all the same size."))
    nm, he, his = P.next()
    its.append(mcq("%s says, “My book is 7 long.” What is missing?" % nm, "the unit",
                   ["a bigger number", "a smaller number", "nothing"],
                   "7 what? 7 cubes and 7 paper clips are not the same length. Say <b>the unit</b>: “7 cubes long”."))
    its.append(mcq("Which units are best for measuring?", "units that are all the same size",
                   ["units of many sizes", "only big units", "units with gaps"],
                   "Use <b>units that are all the same size</b>, laid end to end. Then everyone gets the same count."))
    order = [0, 1, 4, 2, 5, 3, 6, 7, 11, 8, 13, 9, 10, 14, 12, 15, 16, 17, 18, 19]
    assert sorted(order) == list(range(20))
    its = [its[i] for i in order]
    assert len(its) == 20, len(its)
    return {"title": "Same-size units matter", "items": its}


# ============================================================ set 4: compare and order three objects
def set_order(P):
    its = []
    NONE = "They are the same."

    def three(objs, ask, tall=False):
        lens = [L for _, L in objs]
        assert len(set(lens)) == 3
        names = [k for k, _ in objs]
        srt = sorted(objs, key=lambda t: t[1])
        if ask in ("longest", "tallest"):
            ans = srt[-1][0]
        elif ask == "shortest":
            ans = srt[0][0]
        else:
            ans = srt[1][0]
        pic = tall_svg(objs) if tall else compare_svg([(k, 0, L) for k, L in objs])
        if ask == "middle":
            q = fig(pic) + "Which is in the middle? It is not the %s and not the shortest." % ("tallest" if tall else "longest")
        else:
            q = fig(pic) + "Which is the %s?" % ask
        where = "All three stand on the same floor. Look at the tops." if tall else "All three start at the same line. Look at where each one ends."
        e = "%s From shortest to %s: %s. The <b>%s</b> is %s." % (
            where, "tallest" if tall else "longest", ", ".join(k for k, _ in srt), ans,
            "in the middle" if ask == "middle" else "the " + ask)
        return mcq(q, the(ans), [the(n) for n in names if n != ans] + [NONE], e)

    def order(objs, longfirst=False, tall=False):
        srt = sorted(objs, key=lambda t: t[1], reverse=longfirst)
        ans = ", ".join(k for k, _ in srt)
        rev = ", ".join(k for k, _ in reversed(srt))
        sw1 = ", ".join(k for k, _ in [srt[1], srt[0], srt[2]])
        sw2 = ", ".join(k for k, _ in [srt[0], srt[2], srt[1]])
        pic = tall_svg(objs) if tall else compare_svg([(k, 0, L) for k, L in objs])
        a, b = ("tallest", "shortest") if tall and longfirst else ("shortest", "tallest") if tall else \
            ("longest", "shortest") if longfirst else ("shortest", "longest")
        q = fig(pic) + "Put them in order from %s to %s." % (a, b)
        e = "Start with the %s: the %s. Then the %s. Last, the %s. So: <b>%s</b>. Do not start at the wrong end." % (
            a, srt[0][0], srt[1][0], srt[2][0], ans)
        return mcq(q, ans, [rev, sw1, sw2], e)

    its.append(three([("straw", 10), ("key", 3), ("pencil", 7)], "longest"))
    its.append(three([("nail", 5), ("ribbon", 8), ("eraser", 3)], "shortest"))
    its.append(three([("crayon", 6), ("worm", 4), ("marker", 9)], "longest"))
    its.append(three([("leaf", 4), ("craft stick", 8), ("pencil", 6)], "shortest"))
    its.append(three([("crayon", 4), ("straw", 9), ("pencil", 7)], "tallest", tall=True))
    its.append(three([("marker", 6), ("craft stick", 8), ("crayon", 4)], "shortest", tall=True))
    its.append(three([("caterpillar", 7), ("nail", 4), ("straw", 10)], "middle"))
    its.append(three([("pencil", 8), ("crayon", 5), ("marker", 6)], "middle", tall=True))
    its.append(order([("marker", 6), ("strip of paper", 11), ("leaf", 4)]))
    its.append(order([("pencil", 8), ("key", 3), ("ribbon", 5)], longfirst=True))
    its.append(order([("straw", 9), ("crayon", 5), ("craft stick", 7)], tall=True))

    for objs, best, trap in [([("pencil", 0, 7), ("crayon", 4, 5), ("key", 2, 3)], "pencil", "crayon"),
                             ([("marker", 5, 5), ("straw", 0, 8), ("eraser", 1, 3)], "straw", "marker")]:
        lens = {k: L for k, _, L in objs}
        assert max(lens, key=lens.get) == best
        ends = {k: a + L for k, a, L in objs}
        assert max(ends, key=ends.get) == trap
        q = fig(compare_svg(objs, line=False)) + "The ends are not lined up. Which is the longest?"
        e = ("The %s ends furthest along, but it starts later. Slide all three back to one line. "
             "Then the <b>%s is the longest</b>." % (trap, best))
        its.append(mcq(q, the(best), [the(trap)] + [the(k) for k, _, _ in objs if k not in (best, trap)] + [NONE], e))

    q = fig(towers_svg([5, 8, 6])) + "Which cube tower is the tallest?"
    its.append(mcq(q, "tower B", ["tower A", "tower B", "tower C", "They are the same."],
                   "All the towers stand on the same floor. Count the cubes: A has 5, B has 8, C has 6. "
                   "<b>Tower B</b> is the tallest.", lock=True))
    its.append(mcq("A pencil is 7 cubes long. A crayon is 4 cubes long. A straw is 9 cubes long. Which is the longest?",
                   "the straw", ["the pencil", "the crayon", "They are the same."],
                   "They were measured with the same cubes. 9 is the biggest number, so <b>the straw</b> is the longest."))
    its.append(mcq("A ribbon is 6 paper clips long. A string is 3 paper clips long. A scarf is 8 paper clips long. "
                   "Order them from shortest to longest.", "string, ribbon, scarf",
                   ["scarf, ribbon, string", "ribbon, string, scarf", "string, scarf, ribbon"],
                   "Smallest number first: 3, then 6, then 8. So: <b>string, ribbon, scarf</b>."))
    a, b, c = P.next(), P.next(), P.next()
    its.append(mcq("%s’s shoe is 9 cubes long. %s’s shoe is 11 cubes long. %s’s shoe is 8 cubes long. Whose shoe is the shortest?"
                   % (a[0], b[0], c[0]), "%s’s shoe" % c[0], ["%s’s shoe" % a[0], "%s’s shoe" % b[0], "They are the same."],
                   "8 is the smallest number. So <b>%s’s shoe</b> is the shortest. %s’s shoe is the longest." % (c[0], b[0])))
    its.append(mcq("The ribbon is longer than the straw. The straw is longer than the key. Which is the longest?",
                   "the ribbon", ["the straw", "the key", "You cannot tell."],
                   "The ribbon is longer than the straw, and the straw is longer than the key. "
                   "So <b>the ribbon</b> is the longest. The key is the shortest."))
    a, b, c = P.next(), P.next(), P.next()
    its.append(mcq("%s is taller than %s. %s is taller than %s. Who is the shortest?" % (a[0], b[0], b[0], c[0]),
                   c[0], [a[0], b[0], "You cannot tell."],
                   "%s is taller than %s, and %s is taller than %s. From tallest to shortest: %s, %s, %s. "
                   "<b>%s</b> is the shortest." % (a[0], b[0], b[0], c[0], a[0], b[0], c[0], c[0])))
    its.append(mcq("long, longer, ___. Which word comes next?", "longest", ["longer", "short", "shorter"],
                   "Long is one thing. Longer compares two things. <b>Longest</b> is for the one that beats all the others."))
    assert len(its) == 20, len(its)
    return {"title": "Compare and order three objects", "items": its}


# ============================================================ set 5: heavier, holds more, word problems
SAME = "They weigh the same."
CANT = "You cannot tell."


def diff_e(a, b, d):
    e = "Take away the smaller number from the bigger one: %d − %d = <b>%d</b>. " % (a, b, d)
    if 2 <= d <= 5:
        e += "Or count on from %d to %d: %s. That is %d more. " % (b, a, count_list(d, b + 1), d)
    e += "Do not add: %d + %d = %d is both together." % (a, b, a + b)
    return e


def set_problems(P):
    its = []
    ABCD = ["A", "B", "C", "D"]

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
    its.append(pair("brick", "sponge", "L", "lighter"))
    its.append(pair("egg", "shoe", "R", "lighter"))
    its.append(pair("beach ball", "stone", "R", "heavier", trap=True))
    q = fig(balance_svg(("apple", 0), ("orange", 0), "=")) + "The scale is level. Which is true?"
    its.append(mcq(q, SAME, ["The apple is heavier.", "The orange is heavier.", CANT],
                   "The two sides are level. Neither side goes down. So <b>they weigh the same</b>."))
    for kind, n in [("apple", 6), ("toy car", 9)]:
        q = fig(balance_svg((kind, 0), ("cubes", n), "=", labels=[kind, ""])) + "The scale is level. How many cubes balance the %s?" % kind
        e = ("The scale is level, so the cubes weigh the same as the %s. Count the cubes: %s. "
             "<b>%d cubes</b> balance the %s." % (kind, count_list(n), n, kind))
        its.append(mcq_len(q, n, "cube", [n + 1, n - 1, n + 2], e))
    its.append(pair("pillow", "can of beans", "R", "heavier", trap=True))
    its.append(mcq(fig(glasses_svg(["nearly full", "half full", "quarter full", "empty"])) +
                   "The glasses are the same size. Which has the most water?", "A", ABCD,
                   "The glasses are the same size, so look for the highest water. Glass A is nearly full. <b>A</b> has the most.",
                   lock=True))
    its.append(mcq(fig(glasses_svg(["half full", "nearly empty", "full", "quarter full"])) +
                   "The glasses are the same size. Which has the least water?", "B", ABCD,
                   "Look for the lowest water. Glass B is nearly empty. It has less than D. So <b>B</b> has the least.", lock=True))
    its.append(mcq(fig(sizes_svg([(30, 60), (40, 50), (26, 80), (72, 88)])) +
                   "Each container is full. Which one holds the most?", "D", ABCD,
                   "D is the widest and the tallest. So <b>D</b> holds the most. C is tall, but it is thin.", lock=True))
    for n in (4, 7):
        nm, he, his = P.next()
        q = fig(cups_jug_svg(n)) + "%s pours all the cups into the jug. Now the jug is full. How many cups does the jug hold?" % nm
        e = "Count the cups: %s. The jug holds <b>%d cups</b> of water. Do not count the jug." % (count_list(n), n)
        its.append(mcq(q, "%d cups" % n, ["%d cups" % (n + 1), "%d cups" % (n - 1), "%d cups" % (n + 2)], e))

    # word problems
    q = fig(measure2_svg([("pencil", 9), ("crayon", 5)], "cube")) + "How many cubes longer is the pencil than the crayon?"
    its.append(mcq_len(q, 4, "cube", [14, 5, 3, 9], "The pencil is 9 cubes long. The crayon is 5 cubes long. " + diff_e(9, 5, 4)))
    a, b = P.next(), P.next()
    its.append(mcq_len("After a walk in Stanley Park, %s’s stick is 8 cubes long. %s’s stick is 5 cubes long. "
                       "How many cubes longer is %s’s stick?" % (a[0], b[0], a[0]), 3, "cube", [13, 2, 4], diff_e(8, 5, 3)))
    its.append(mcq_len("A toy orca balances 12 cubes. A toy salmon balances 7 cubes. How many cubes heavier is the orca?",
                       5, "cube", [19, 6, 4], diff_e(12, 7, 5)))
    a, b = P.next(), P.next()
    its.append(mcq("At recess, %s builds a tower 9 blocks tall. %s’s tower is 4 blocks taller. How tall is %s’s tower?"
                   % (a[0], b[0], b[0]), "13 blocks", ["5 blocks", "9 blocks", "12 blocks"],
                   "“4 blocks taller” means add 4. 9 + 4 = <b>13</b>. It is taller, so the number must be bigger than 9."))
    nm, he, his = P.next()
    its.append(mcq("At a beach in Victoria, %s fills a pail with 9 cups of water. %s pours out 3 cups. How many cups are left?"
                   % (nm, cap(he)), "6 cups", ["12 cups", "5 cups", "7 cups"],
                   "Pouring out means take away. 9 − 3 = <b>6</b>. There are 6 cups left. Do not add: 9 + 3 = 12."))
    nm, he, his = P.next()
    its.append(mcq_len("%s needs 12 cubes to balance %s lunch box. %s has put 9 cubes on the scale. How many more cubes does %s need?"
                       % (nm, his, cap(he), he), 3, "cube", [21, 2, 4],
                       "Count on from 9 to 12: 10, 11, 12. That is 3. Or 12 − 9 = <b>3</b>. Check: 9 + 3 = 12."))
    nm, he, his = P.next()
    its.append(mcq("On a hot day in Kelowna, %s fills a watering can with 4 cups, then 5 more cups. Now it is full. "
                   "How many cups does it hold?" % nm, "9 cups", ["1 cup", "8 cups", "10 cups"],
                   "First 4 cups, then 5 more. Add: 4 + 5 = <b>9</b>. The watering can holds 9 cups. "
                   "Do not take away: 5 − 4 = 1."))
    assert len(its) == 20, len(its)
    return {"title": "Heavier, holds more and word problems", "items": its}


# ============================================================ lesson
def body_html():
    return (
        "<h2>Line up the ends</h2>"
        "<p>Put two things side by side. Line up one end. Look at the other end. "
        "The one that sticks out is <b>longer</b>. The other is <b>shorter</b>. "
        "For things that stand up, we say <b>taller</b>.</p>"
        "<figure class='sn-fig'>" + compare_svg([("pencil", 0, 8), ("crayon", 0, 5)]) +
        "<figcaption>Both start at the same line. The pencil is longer. The crayon is shorter.</figcaption></figure>"
        "<h2>Measure with cubes or paper clips</h2>"
        "<p>Lay cubes along the object, <b>end to end</b>. Start right at one end. Stop at the other end. "
        "Count the cubes. Say the unit too: “6 cubes long”.</p>"
        "<figure class='sn-fig'>" + measure_svg("crayon", 6, "cube") +
        "<figcaption>6 cubes fit from one end of the crayon to the other. The crayon is 6 cubes long.</figcaption></figure>"
        "<p>Two rules: <b>no gaps</b> and <b>no overlaps</b>.</p>"
        "<figure class='sn-fig'>" + wrong_svg("crayon", 4, "clip", "gap") +
        "<figcaption>Wrong: there are gaps. Only 3 paper clips are counted, but the crayon is 4 paper clips long.</figcaption></figure>"
        "<h2>Use units that are all the same</h2>"
        "<p>Use one kind of unit. A paper clip is longer than a cube. "
        "So fewer paper clips fit. <b>Bigger units give a smaller number.</b></p>"
        "<figure class='sn-fig'>" + two_units_svg("pencil", 8) +
        "<figcaption>The same pencil is 8 cubes long and 4 paper clips long.</figcaption></figure>"
        + ex("Order three things", "A straw is 10 cubes long. A key is 3 cubes long. A pencil is 7 cubes long. "
             "Order them from shortest to longest.", "Find the smallest number first: 3, then 7, then 10.",
             "key, pencil, straw")
        + "<h2>Heavier and holds more</h2>"
        "<p>Put two things on a balance. The <b>heavier</b> side goes down. "
        "If the sides are level, they weigh the same. "
        "To see which container <b>holds more</b>, fill each one with the same cup and count.</p>"
        "<figure class='sn-fig'>" + balance_svg(("beach ball", 0), ("stone", 0), "R") +
        "<figcaption>The stone side is down, so the stone is heavier. The beach ball is bigger, but it is lighter.</figcaption></figure>"
        + ex("How many longer?", "A pencil is 9 cubes long. A crayon is 5 cubes long. How many cubes longer is the pencil?",
             "9 − 5 = 4. Or count on from 5: 6, 7, 8, 9. That is 4.", "4 cubes")
        + "<h2>Common mistakes</h2>"
        + table(["Mistake", "What to do instead"], [
            ["Not lining up the ends", "Start both objects at the same line"],
            ["Starting the cubes past the end", "Put the first cube right at one end"],
            ["Leaving gaps between cubes", "Push the cubes together so they touch"],
            ["Overlapping paper clips", "Lay them end to end, not on top"],
            ["Mixing cubes and paper clips", "Use one kind of unit all the way"],
            ["Thinking bigger means heavier", "Use a balance: the side that goes down is heavier"],
        ])
    )


FAQ = [
    {"q": "What measurement do Grade 1 students learn in the BC math curriculum?",
     "a": "BC Grade 1 students learn direct measurement with non-standard units. They compare and order objects by length, "
          "mass and capacity, and measure length with units like cubes and paper clips."},
    {"q": "What are non-standard units of measurement?",
     "a": "Non-standard units are everyday objects used to measure, like linking cubes, paper clips, hand spans or cups. "
          "They show children that a length is how many units fit along an object, before they use rulers."},
    {"q": "Why should the units be the same size?",
     "a": "Units of different sizes make the count meaningless: 6 paper clips is longer than 6 cubes. "
          "Same-size units laid with no gaps or overlaps let two people get the same answer."},
    {"q": "How can I practise measuring with my Grade 1 child at home?",
     "a": "Measure a book or a rain boot with LEGO bricks laid end to end, compare two things on a coat hanger balance, "
          "and count cups of water to see which container holds more."},
]


def gen():
    rnd = random.Random(51807)
    P = People(rnd)
    sets = [set_compare(P), set_units(P), set_same_units(P), set_order(P), set_problems(P)]
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
            m = re.search(r"aria-label='([a-z ]+) measured with (\d+) cubes and with (\d+) paper clips'", it["q"])
            if m and "How many" in it["q"]:
                want = "%s paper clips" % m.group(3) if "paper clips long is it" in it["q"] else "%s cubes" % m.group(2)
                assert ans == want, (ans, want)
                n += 1
            m = re.search(r"aria-label='cube towers: ([^']+)'", it["q"])
            if m:
                hs = [int(x) for x in re.findall(r"(\d+) cubes", m.group(1))]
                assert ans == "tower " + "ABC"[hs.index(max(hs))]
                n += 1
            m = re.search(r"aria-label='objects (?:side by side|standing on the floor): ([^']+)'", it["q"])
            if m and re.search(r"Which is the (longest|shortest|tallest)\?|in the middle", it["q"]):
                if "from" in m.group(1):
                    objs = [(x.group(1), int(x.group(3)) - int(x.group(2))) for x in re.finditer(r"([a-z ]+?) from (\d+) to (\d+)", m.group(1))]
                else:
                    objs = [(x.group(1), int(x.group(2))) for x in re.finditer(r"([a-z ]+?) (\d+) high", m.group(1))]
                objs = [(k.strip(", "), L) for k, L in objs]
                srt = sorted(objs, key=lambda t: t[1])
                if "in the middle" in it["q"]:
                    want = srt[1][0]
                elif "shortest?" in it["q"]:
                    want = srt[0][0]
                else:
                    want = srt[-1][0]
                assert ans == "the " + want, (ans, want)
                n += 1
    assert n == 12 + 5 + 2 + 2 + 4 + 1 + 10, n
    for it in sets[4]["items"]:
        m = re.search(r"with ([a-z ]+) on the left and ([a-z ]+) on the right, the (left|right) side is down'", it["q"])
        if m and "Which is heavier" in it["q"]:
            assert it["c"][it["a"]] == "the " + (m.group(1) if m.group(3) == "left" else m.group(2))
        if m and "Which is lighter" in it["q"]:
            assert it["c"][it["a"]] == "the " + (m.group(2) if m.group(3) == "left" else m.group(1))
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
        "country": "ca-bc", "subject": "math", "grade": "grade-1", "slug": "measuring-with-non-standard-units", "sort": 7,
        "updated": UPDATED, "pdf_url": "",
        "title": "Measuring with Non-Standard Units",
        "seo_title": "Grade 1 Measuring with Non-Standard Units Worksheets (Free, BC Curriculum, Answer Key)",
        "short_title": "Measuring with non-standard units",
        "domain": "Geometry and measurement",
        "standard_code": "Grade 1: Geometry and measurement",
        "standard_url": "https://curriculum.gov.bc.ca/curriculum/mathematics/1/core",
        "standard_text": "Direct measurement with non-standard units (non-uniform and uniform)",
        "meta_desc": "Free Grade 1 math worksheets on measuring with non-standard units for the BC curriculum: "
                     "longer, shorter and taller, measuring with cubes and paper clips with no gaps or overlaps, "
                     "why same-size units matter, ordering three objects, and heavier and holds more. "
                     "100 picture questions with an answer key.",
        "key_big": "Line up the ends. Lay units end to end: no gaps, no overlaps, all the same size.",
        "key_sub": "Count the units from one end to the other and say the unit: “6 cubes long”. "
                   "A paper clip is longer than a cube, so fewer paper clips fit. Only compare counts made with the same unit.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }


if __name__ == "__main__":
    out = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, out["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(out, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
