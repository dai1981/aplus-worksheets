# -*- coding: utf-8 -*-
"""
AU Year 2 Maths: Measuring Length, Mass and Capacity (Australian Curriculum v9.0, AC9M2M01)
  python tools/gen_au_maths_y2_measuring.py
Measure and compare with uniform informal units: cubes and paper clips for length, cubes on a balance for mass,
cups for capacity, and smaller units for accuracy. Australian English, short sentences for 7 to 8 year olds.
Every picture is drawn exactly from the data: a paper clip is exactly 2 cubes long, objects run from one cube
boundary to another, the heavier side of a balance is the lower one, and containers are straight-sided.
Wrong answers come from real mistakes: gaps or overlaps between units, starting past the end, mixing units of
different sizes, counting the lines between cubes or the extra cubes, using different-size hands or feet,
thinking a bigger unit gives a bigger number, thinking bigger means heavier and thinking taller holds more.
HTML attributes use single quotes (no backslashes in the JSON).
"""
import json, os, random, re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "au", "maths", "year-2")
UPDATED = "2026-11-02"
GREEN = "#006633"
INK = "#2b2b2b"
GREY = "#8a8a8a"
WATER = "#9fd3f2"
WATER_LINE = "#2a7fb8"
FONT = "Arial, Helvetica, sans-serif"
GIRLS = ["Charlotte", "Isla", "Mia", "Amelia", "Ava", "Harper", "Chloe", "Ruby", "Mei", "Zara", "Matilda", "Sienna",
         "Grace"]
BOYS = ["Oliver", "Jack", "Noah", "William", "Leo", "Lachlan", "Liam", "Aarav", "Kai", "Cooper", "Ethan"]

PX = 24                       # one cube = one grid step
PU = {"cube": 24, "clip": 48}  # a paper clip is exactly 2 cubes long in every picture
UNAME = {"cube": ("cube", "cubes"), "clip": ("paper clip", "paper clips"), "cup": ("cup", "cups"),
         "step": ("footstep", "footsteps"), "hand": ("handspan", "handspans")}
CUBE_COLOURS = ["#e05a6a", "#3d7cc9"]
BAND = 24


def u(n, unit):
    one, many = UNAME[unit]
    return "%d %s" % (n, one if n == 1 else many)


# ------------------------------------------------------------ helpers
def mcq(q, correct, cands, e, lock=False):
    """4 choices: correct + the first 3 unique distractors. lock=True keeps the order (A-D picture labels)."""
    correct = str(correct)
    if lock:
        assert cands == ["A", "B", "C", "D"] and correct in cands
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
    elif kind == "gum leaf":
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
    elif kind == "rubber":
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


def mixed_svg(kind, pattern):
    """The object measured with a row that mixes paper clips and cubes (end to end, no gaps)."""
    L = sum(2 if p == "clip" else 1 for p in pattern)
    x0, x1 = PADL, PADL + L * PX
    y = 6
    s = [guide(x0, y - 3, y + 2 * BAND + 8), guide(x1, y - 3, y + 2 * BAND + 8), draw_object(kind, x0, x1, y, y + BAND)]
    x = x0
    for i, p in enumerate(pattern):
        if p == "clip":
            s.append(draw_object("paper clip", x, x + PU["clip"], y + BAND + 6, y + 2 * BAND + 6))
            x += PU["clip"]
        else:
            s.append(cube(x, y + BAND + 6, i))
            x += PU["cube"]
    assert x == x1
    return svg_wrap(int(x1 + PADL), y + 2 * BAND + 12, "".join(s),
                    "%s measured with %d paper clips and cubes mixed together" % (kind, len(pattern)), lg=True)


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
                    "%s between %d and %d paper clips long" % (kind, n - 1, n), lg=True)


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
THING_H = {"apple": 37, "orange": 26, "pear": 43, "banana": 18, "feather": 22, "book": 22, "brick": 22, "sponge": 20,
           "beach ball": 56, "stone": 18, "pillow": 28, "tin of beans": 33, "toy car": 26, "teddy": 48, "shoe": 20,
           "egg": 26, "watermelon": 40, "lunch box": 30}


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
    elif kind == "tin of beans":
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
    elif kind == "lunch box":
        s.append("<rect x='%.1f' y='%.1f' width='56' height='26' rx='4' fill='#5dade2' stroke='%s' stroke-width='1.3'/>" % (cx - 28, b - 26, INK))
        s.append("<path d='M%.1f %.1f v-4 h20 v4' fill='none' stroke='%s' stroke-width='2'/>" % (cx - 10, b - 26, INK))
        s.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='1.2'/>" % (cx - 28, b - 17, cx + 28, b - 17, INK))
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


def thing_h(kind, n):
    return ((n + 3) // 4) * SC if kind == "cubes" else THING_H[kind]


def balance_svg(left, right, tilt, labels=None):
    """left/right: (kind, n). tilt: 'L' (left side down), 'R' (right side down) or '=' (level)."""
    W, cx, half, d = 280, 140, 80, 16
    dl = {"L": d, "R": -d, "=": 0}[tilt]
    # room above the higher pan for the tallest thing
    need = max(thing_h(k, n) + 11 - dd for (k, n), dd in [(left, dl), (right, -dl)])
    py = max(84, need + 6)
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
        assert top - 1 - thing_h(kind, n) >= 2, (kind, n)
        names.append("%d cubes" % n if kind == "cubes" else kind)
    if labels is None:
        labels = names
    for lab, x in zip(labels, (cx - half, cx + half)):
        if lab:
            s.append(text(x, py + 78, lab, 15))
    word = {"L": "the left side is down", "R": "the right side is down", "=": "the two sides are level"}[tilt]
    return svg_wrap(W, py + 86, "".join(s), "balance scale with %s on the left and %s on the right, %s" % (names[0], names[1], word), lg=True)


# ------------------------------------------------------------ containers
def container(x, b, w, h, frac):
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


def glasses_svg(states, labels="ABCD"):
    w, h, gap = 44, 84, 30
    s = []
    for i, st in enumerate(states):
        x = 16 + i * (w + gap)
        s.append(container(x, h + 10, w, h, LEVEL[st]))
        s.append(text(x + w / 2.0, h + 32, labels[i], 18 if isinstance(labels, str) else 14))
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


def cups_jug_svg(n, what="jug"):
    """An empty container and n full cups (rows of up to 5, stacked upwards)."""
    jw, jh = 64, 96
    cw, ch = 24, 30
    rows = [min(5, n - r * 5) for r in range((n + 4) // 5)]
    b = max(jh + 10, len(rows) * (ch + 14) + 4)
    s = [container(16, b, jw, jh, 0.0)]
    if what == "jug":
        s.append("<path d='M%d %d C%d %d %d %d %d %d' fill='none' stroke='%s' stroke-width='3'/>"
                 % (16 + jw, b - jh + 20, 16 + jw + 20, b - jh + 20, 16 + jw + 20, b - 40, 16 + jw, b - 40, INK))
    s.append(text(16 + jw / 2.0, b + 22, what, 15))
    x0 = 16 + jw + 44
    for r, k in enumerate(rows):
        for i in range(k):
            s.append(container(x0 + i * (cw + 10), b - r * (ch + 14), cw, ch, 0.8))
    W = x0 + max(rows) * (cw + 10) - 10 + 16
    return svg_wrap(W, b + 30, "".join(s), "an empty %s and %d cups of water" % (what, n), lg=True)


# ============================================================ set 1: measure length with cubes and paper clips
S1 = [("crayon", 5, "cube", None), ("key", 3, "cube", None), ("pencil", 8, "cube", None),
      ("rubber", 2, "clip", None), ("ribbon", 10, "cube", None), ("gum leaf", 3, "clip", None),
      ("straw", 12, "cube", None), ("marker", 4, "clip", None), ("caterpillar", 7, "cube", None),
      ("strip of paper", 6, "clip", None), ("craft stick", 6, "cube", 9), ("worm", 9, "cube", 12)]

OK = "Yes, it is right."
GAP = "No, there are gaps."
OVER = "No, they overlap."
START = "No, the start is wrong."
MIXED = "No, the units are not the same."
MODE_ANS = {"exact": OK, "gap": GAP, "overlap": OVER, "late": START, "mixed": MIXED}


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

    for kind, L, unit, mode in [("pencil", 7, "cube", "exact"), ("crayon", 4, "clip", "gap"),
                                ("ribbon", 7, "clip", "overlap"), ("straw", 6, "cube", "late")]:
        q = fig(wrong_svg(kind, L, unit, mode)) + "Is this the right way to measure the %s?" % kind
        un = UNAME[unit][1]
        if mode == "exact":
            e = ("Yes. The %s start at one end of the %s and stop at the other end. They touch with no gaps. "
                 "They are all the same size. The %s is <b>%s</b> long." % (un, kind, kind, u(L, unit)))
        elif mode == "gap":
            e = ("<b>No, there are gaps</b> between the %s. The gaps are not counted, so the number is too small. "
                 "Push the %s together so they touch." % (un, un))
        elif mode == "overlap":
            e = "<b>No, the %s overlap</b>. Some lie on top of others, so you count too many. Lay them end to end." % un
        else:
            e = ("<b>No, the start is wrong.</b> The first %s does not start at the end of the %s. "
                 "Line up the first one with the end of the %s." % (UNAME[unit][0], kind, kind))
        its.append(mcq(q, MODE_ANS[mode], [x for x in [OK, GAP, OVER, START, MIXED] if x != MODE_ANS[mode]][:3], e))

    pat = ["clip", "cube", "clip", "cube", "clip", "cube"]
    its.append(mcq(fig(mixed_svg("marker", pat)) + "Is this the right way to measure the marker?", MIXED,
                   [OK, GAP, OVER],
                   "<b>No, the units are not the same.</b> Some are paper clips and some are cubes. "
                   "A paper clip is longer than a cube, so “6 units” does not tell us the length. "
                   "Use only cubes or only paper clips."))

    for kind, L, mode, ans, e in [
        ("pencil", 5, "gap", "too small",
         "The gaps between the paper clips are not counted. So the number is <b>too small</b>. "
         "The pencil is really longer than the count."),
        ("ribbon", 4, "overlap", "too big",
         "The paper clips lie on top of each other, so there are too many under the ribbon. "
         "The number is <b>too big</b>."),
    ]:
        n = n_gap(L, "clip") if mode == "gap" else n_over(L, "clip")
        q = (fig(wrong_svg(kind, L, "clip", mode)) +
             "%s counts %d paper clips. Is the count too big or too small?" % (P.next()[0], n))
        its.append(mcq(q, ans, ["too big" if ans == "too small" else "too small", "just right", "You cannot tell."], e))

    its.append(mcq("You measure a crayon with cubes. What do you count?", "the cubes under it",
                   ["all the cubes in the box", "the lines between cubes", "the colours of the cubes"],
                   "Lay cubes along the crayon from end to end. Count only <b>the cubes under the crayon</b>. "
                   "That number is its length."))
    order = [0, 1, 2, 3, 4, 18, 5, 6, 7, 13, 8, 14, 9, 10, 15, 16, 11, 12, 17, 19]
    assert sorted(order) == list(range(len(its)))
    its = [its[i] for i in order]
    assert len(its) == 20, len(its)
    return {"title": "Measure length with cubes and paper clips", "items": its}


# ============================================================ set 2: choose a unit; smaller units for accuracy
def set_choose(P):
    its = []
    for kind, cubes in [("pencil", 8), ("ribbon", 10), ("straw", 12), ("crayon", 6)]:
        clips = cubes // 2
        q = fig(two_units_svg(kind, cubes)) + "The %s is %d cubes long. How many paper clips long is it?" % (kind, cubes)
        e = ("Look at the bottom row. Count the paper clips under the %s: %s. It is <b>%s</b> long. "
             "A paper clip is longer than a cube, so you need fewer of them." % (kind, count_list(clips), u(clips, "clip")))
        its.append(mcq_len(q, clips, "clip", [cubes, cubes * 2, clips + 1], e))
    q = fig(two_units_svg("strip of paper", 14)) + "The strip of paper is 7 paper clips long. How many cubes long is it?"
    its.append(mcq_len(q, 14, "cube", [7, 9, 13],
                       "Look at the middle row. Count the cubes: 1 to 14. It is <b>14 cubes</b> long. "
                       "A cube is shorter than a paper clip, so you need more cubes."))
    its.append(mcq("A pencil is 10 cubes long. It is 5 paper clips long. Why are there more cubes?",
                   "A cube is shorter.", ["A cube is longer.", "The pencil got longer.", "Someone made a mistake."],
                   "Each cube is shorter than a paper clip, so it takes <b>more cubes</b> to cover the same pencil. "
                   "Smaller unit, bigger number."))
    a, b = P.next(), P.next()
    its.append(mcq("%s measures a book with cubes and gets 12. %s measures it with paper clips and gets 6. Who is right?"
                   % (a[0], b[0]), "They are both right.", [a[0], b[0], "Neither of them."],
                   "A paper clip is 2 cubes long. 6 paper clips is the same length as 12 cubes. "
                   "<b>They are both right</b>. They used different units."))
    its.append(mcq("You measure a desk with cubes and then with paper clips. Which gives the bigger number?", "cubes",
                   ["paper clips", "They give the same number.", "You cannot tell."],
                   "A cube is smaller than a paper clip. You need more small units to cover the desk, "
                   "so <b>cubes</b> give the bigger number."))
    for kind, cubes in [("pencil", 7), ("marker", 5), ("ribbon", 9)]:
        n = cubes // 2
        q = fig(about_svg(kind, cubes)) + "The paper clips do not fit exactly. How long is the %s?" % kind
        e = ("%d paper clips are not long enough. %d paper clips go past the end. So the %s is "
             "<b>between %d and %d paper clips</b> long. Measure with smaller units, like cubes, to be exact."
             % (n, n + 1, kind, n, n + 1))
        its.append(mcq(q, "between %d and %d paper clips" % (n, n + 1),
                       [u(n + 1, "clip"), u(n, "clip"), u(cubes, "clip")], e))
    q = fig(about_svg("crayon", 5)) + "How can you measure the crayon more exactly?"
    its.append(mcq(q, "Use smaller units, like cubes.",
                   ["Use bigger units, like footsteps.", "Count the last clip as 1.", "Leave out the last clip."],
                   "The crayon is between 2 and 3 paper clips. <b>Smaller units</b> fit more closely, "
                   "so cubes tell us the length more exactly. The crayon is 5 cubes long."))
    for obj, ans, wr, e in [
        ("the length of the classroom", "footsteps", ["paper clips", "cubes", "cups"],
         "The classroom is long. Paper clips or cubes would take a very long time. "
         "<b>Footsteps</b> are a good unit for long things. Cups are for capacity, not length."),
        ("the length of a rubber", "cubes", ["footsteps", "handspans", "cups"],
         "A rubber is short. A footstep or a handspan is too big. <b>Cubes</b> are small, "
         "so they fit and give an exact count."),
        ("the length of a desk", "handspans", ["footsteps", "cups", "buckets"],
         "A desk is not very long. <b>Handspans</b> fit along it well. Cups and buckets measure capacity."),
        ("the length of the netball court", "footsteps", ["handspans", "paper clips", "cubes"],
         "A netball court is very long. Big units are best for long things, so use <b>footsteps</b>."),
    ]:
        its.append(mcq("Which unit is best for measuring %s?" % obj, ans, wr, e))
    a, b = P.next(), P.next()
    its.append(mcq("%s and %s both measure the same desk in handspans. %s gets 8. %s gets 10. Why?"
                   % (a[0], b[0], a[0], b[0]), "Their hands are different sizes.",
                   ["The desk changed.", "%s counted wrong." % a[0], "Handspans are always 10."],
                   "%s’s hand is bigger, so fewer handspans fit. Units of <b>different sizes</b> give different "
                   "numbers. That is why we use units that are all the same, like cubes." % a[0]))
    its.append(mcq("Why do we use units that are all the same size?", "So everyone gets the same answer.",
                   ["So it looks neat.", "So we need more units.", "So it is quicker to count."],
                   "If the units are all the same, anyone who measures the same thing gets the same number. "
                   "<b>So everyone gets the same answer</b>."))
    its.append(mcq("A rope is 6 footsteps long. A ribbon is 6 paper clips long. Which is longer?", "the rope",
                   ["the ribbon", "They are the same.", "You cannot tell."],
                   "Both numbers are 6, but the units are different. A footstep is much longer than a paper clip. "
                   "So <b>the rope</b> is longer. Always check the unit."))
    nm, he, his = P.next()
    its.append(mcq_len("A paper clip is as long as 2 cubes. %s’s book is 10 cubes long. How many paper clips long is it?" % nm,
                       5, "clip", [10, 20, 8],
                       "Each paper clip covers 2 cubes. Count in 2s to 10: 2, 4, 6, 8, 10. That is 5 jumps. "
                       "The book is <b>5 paper clips</b> long."))
    order = [0, 1, 2, 5, 3, 6, 7, 8, 9, 10, 11, 12, 13, 4, 14, 15, 16, 17, 18, 19]
    assert sorted(order) == list(range(len(its)))
    its = [its[i] for i in order]
    assert len(its) == 20, len(its)
    return {"title": "Choose units: same size and smaller for accuracy", "items": its}


# ============================================================ set 3: mass on a balance
def set_mass(P):
    its = []
    SAME = "They weigh the same."
    CANT = "You cannot tell."

    def pair(a, b, tilt, ask, trap=None):
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
            e += " The %s looks bigger, but bigger is not always heavier." % trap
        return mcq(q, the(win), [the(lose), SAME, CANT], e)

    its.append(pair("book", "feather", "L", "heavier"))
    its.append(pair("orange", "watermelon", "R", "heavier"))
    its.append(pair("brick", "sponge", "L", "lighter"))
    its.append(pair("egg", "shoe", "R", "lighter"))
    its.append(pair("beach ball", "stone", "R", "heavier", trap="beach ball"))
    its.append(pair("tin of beans", "pillow", "L", "lighter", trap="pillow"))
    q = fig(balance_svg(("apple", 0), ("orange", 0), "=")) + "The scale is level. Which is true?"
    its.append(mcq(q, SAME, ["The apple is heavier.", "The orange is heavier.", CANT],
                   "The two sides are level. Neither side goes down. So <b>they weigh the same</b>."))

    for kind, n in [("apple", 8), ("banana", 6), ("toy car", 11), ("teddy", 14), ("shoe", 13)]:
        q = fig(balance_svg((kind, 0), ("cubes", n), "=", labels=[kind, ""])) + "The scale is level. How many cubes balance the %s?" % kind
        rows = (n + 3) // 4
        e = ("The scale is level, so the cubes weigh the same as the %s. Count the cubes: %s. "
             "<b>%d cubes</b> balance the %s." % (kind, count_list(n), n, kind))
        if rows > 1:
            e += " Count every row, not just the bottom row."
        its.append(mcq_len(q, n, "cube", [n + 1, n - 1, 4 if rows > 1 else n + 2, n + 2], e))

    q = fig(balance_svg(("orange", 0), ("cubes", 4), "L", labels=["orange", "4 cubes"])) + "Which is true?"
    its.append(mcq(q, "The orange is heavier than 4 cubes.",
                   ["The orange is lighter than 4 cubes.", "The orange weighs the same as 4 cubes.", CANT],
                   "The orange side goes down. The side that goes down is heavier. So <b>the orange is heavier than 4 cubes</b>."))
    q = fig(balance_svg(("pear", 0), ("cubes", 10), "R", labels=["pear", "10 cubes"])) + "Which is true?"
    its.append(mcq(q, "The pear is lighter than 10 cubes.",
                   ["The pear is heavier than 10 cubes.", "The pear weighs the same as 10 cubes.", CANT],
                   "The pear side goes up. The side that goes up is lighter. So <b>the pear is lighter than 10 cubes</b>. "
                   "Take some cubes off to make it level."))
    nm, he, his = P.next()
    q = fig(balance_svg(("apple", 0), ("cubes", 7), "=", labels=["apple", "7 cubes"]))
    its.append(mcq(q + "%s adds 1 more cube to the cubes side. What happens?" % nm, "The cubes side goes down.",
                   ["The apple side goes down.", "The sides stay level.", "Both sides go up."],
                   "Now the cubes side is heavier than the apple. The heavier side goes down, so "
                   "<b>the cubes side goes down</b>."))

    its.append(mcq("A brick and a sponge are on a balance. The brick is heavier. Which side goes down?",
                   "the brick side", ["the sponge side", "Both go down.", "Neither side."],
                   "The heavier thing makes its side go down. The brick is heavier, so <b>the brick side</b> goes down."))
    nm, he, his = P.next()
    its.append(mcq("%s thinks the beach ball is heavier because it is bigger. On the balance, the beach ball side goes up. "
                   "Is %s right?" % (nm, he),
                   "No, the ball is lighter.", ["Yes, the ball is heavier.", SAME, CANT],
                   "The side that goes up is lighter. So the beach ball is lighter. "
                   "<b>%s is not right</b>. Big things can be light." % nm))
    its.append(mcq("The watermelon is heavier than the pineapple. The pineapple is heavier than the apple. Which is the lightest?",
                   "the apple", ["the watermelon", "the pineapple", CANT],
                   "From heaviest to lightest: watermelon, pineapple, apple. <b>The apple</b> is the lightest."))
    its.append(mcq("The tin is lighter than the bag. The bag is lighter than the box. Which is the heaviest?",
                   "the box", ["the tin", "the bag", CANT],
                   "Each one is lighter than the next. From lightest: tin, bag, box. So <b>the box</b> is the heaviest. "
                   "Read “lighter” carefully."))
    its.append(mcq("An apple balances 8 cubes. The same apple balances 4 marbles. Which is heavier: 1 cube or 1 marble?",
                   "1 marble", ["1 cube", SAME, CANT],
                   "It takes fewer marbles than cubes to balance the same apple. So each marble must be heavier. "
                   "<b>1 marble</b> is heavier than 1 cube."))
    order = [0, 1, 2, 3, 6, 16, 4, 5, 17, 7, 8, 12, 9, 10, 13, 14, 11, 15, 18, 19]
    assert sorted(order) == list(range(len(its)))
    its = [its[i] for i in order]
    assert len(its) == 20, len(its)
    return {"title": "Heavier, lighter and balancing cubes", "items": its}


# ============================================================ set 4: capacity with cups and jugs
def set_capacity(P):
    its = []
    for n, what in [(5, "jug"), (8, "jug"), (11, "bucket"), (13, "jug")]:
        nm, he, his = P.next()
        q = (fig(cups_jug_svg(n, what)) +
             "%s pours all the cups into the %s. Now the %s is full. How many cups does the %s hold?" % (nm, what, what, what))
        e = "Count the cups: %s. The %s holds <b>%d cups</b> of water. Do not count the %s." % (count_list(n), what, n, what)
        its.append(mcq(q, "%d cups" % n, ["%d cups" % (n + 1), "%d cups" % (n - 1), "%d cups" % (n + 2)], e))

    ABCD = ["A", "B", "C", "D"]
    its.append(mcq(fig(sizes_svg([(34, 60), (70, 90), (24, 90), (50, 40)])) +
                   "Each container is full. Which one holds the most?", "B", ABCD,
                   "B is the widest and as tall as C. C is tall but very thin. So <b>B</b> holds the most. "
                   "Tall does not always mean it holds more.", lock=True))
    its.append(mcq(fig(sizes_svg([(40, 70), (60, 50), (24, 30), (34, 90)])) +
                   "Each container is full. Which one holds the least?", "C", ABCD,
                   "C is the thinnest and the shortest. So <b>C</b> holds the least.", lock=True))
    its.append(mcq(fig(glasses_svg(["half full", "nearly empty", "quarter full", "nearly full"])) +
                   "The glasses are the same size. Which glass has the most water?", "D", ABCD,
                   "The glasses are the same size, so look for the highest water. Glass D is nearly full. "
                   "<b>D</b> has the most.", lock=True))
    its.append(mcq(fig(glasses_svg(["quarter full", "full", "nearly empty", "half full"])) +
                   "The glasses are the same size. Which glass has the least water?", "C", ABCD,
                   "Look for the lowest water. Glass C is nearly empty. It has less than A, which is quarter full. "
                   "So <b>C</b> has the least.", lock=True))
    its.append(mcq(fig(glasses_svg(["half full", "quarter full", "nearly full", "empty"])) +
                   "The glasses are the same size. Which glass is half full?", "A", ABCD,
                   "Half full means the water comes up to the middle. Glass C is nearly full, not half full. "
                   "Glass B is quarter full. <b>A</b> is half full.", lock=True))

    for q, ans, wr, e in [
        ("Which unit is best for measuring how much a bath holds?", "buckets",
         ["teaspoons", "paper clips", "handspans"],
         "A bath holds a lot of water. Teaspoons would take far too long. <b>Buckets</b> are a big unit for a big container. "
         "Paper clips and handspans measure length."),
        ("Which unit is best for measuring how much a drink bottle holds?", "cups",
         ["buckets", "footsteps", "cubes"],
         "A drink bottle is small. A bucket is far too big. <b>Cups</b> fit well. Footsteps measure length."),
    ]:
        its.append(mcq(q, ans, wr, e))

    a, b = P.next(), P.next()
    its.append(mcq("%s fills a bucket with big cups. %s fills the same bucket with small cups. Who needs more cups?"
                   % (a[0], b[0]), b[0], [a[0], "They need the same.", "You cannot tell."],
                   "Small cups hold less, so you need more of them to fill the same bucket. "
                   "<b>%s</b> needs more cups." % b[0]))
    its.append(mcq("A jug holds 6 cups. You use a smaller cup to fill it. Will you need more or fewer cups?",
                   "more cups", ["fewer cups", "6 cups", "the same number"],
                   "A smaller cup holds less each time. So it takes <b>more cups</b> to fill the jug. "
                   "Smaller unit, bigger number."))
    nm, he, his = P.next()
    its.append(mcq("A big cup holds as much as 2 small cups. A jug holds 6 big cups. How many small cups does it hold?",
                   "12 small cups", ["3 small cups", "6 small cups", "8 small cups"],
                   "Each big cup is 2 small cups. 6 lots of 2: 2, 4, 6, 8, 10, 12. "
                   "The jug holds <b>12 small cups</b>."))
    nm, he, his = P.next()
    its.append(mcq("%s fills a tall, thin vase with water. %s pours it all into a short, wide bowl. "
                   "The bowl is not full. Which holds more?" % (nm, cap(he)),
                   "the bowl", ["the vase", "They hold the same.", "You cannot tell."],
                   "All the water from the vase fits in the bowl, with room to spare. "
                   "So <b>the bowl</b> holds more. Taller does not always mean it holds more."))
    nm, he, his = P.next()
    its.append(mcq("%s fills a bottle with water. %s pours it into a jug. The water spills over the top of the jug. "
                   "Which holds more?" % (nm, cap(he)),
                   "the bottle", ["the jug", "They hold the same.", "You cannot tell."],
                   "The water from the bottle is too much for the jug. So <b>the bottle</b> holds more."))
    its.append(mcq("When you use a cup to fill a jug, how full should each cup be?", "full to the top",
                   ["half full", "nearly empty", "any amount"],
                   "Each cup must hold the same amount, so fill it <b>full to the top</b> every time. "
                   "Then every cup is the same unit."))
    nm, he, his = P.next()
    its.append(mcq("%s fills a jug with half-full cups. %s counts 10 cups. Will the jug hold 10 full cups?" % (nm, cap(he)),
                   "No, fewer full cups.", ["Yes, 10 full cups.", "No, more full cups.", "You cannot tell."],
                   "Each cup was only half full, so each one held less. 2 half cups make 1 full cup. "
                   "The jug holds <b>fewer full cups</b>: only 5."))
    its.append(mcq(fig(cups_jug_svg(8)) + "These 8 cups fill the jug. How many cups make the jug half full?",
                   "4 cups", ["8 cups", "16 cups", "2 cups"],
                   "Half of 8 is 4, because 4 + 4 = 8. So <b>4 cups</b> fill the jug half way. "
                   "16 would be double."))
    its.append(mcq("Jug A holds 7 cups. Bottle B holds 5 cups. Both use the same cup. Which holds more?", "jug A",
                   ["bottle B", "They hold the same.", "You cannot tell."],
                   "They were measured with the same cup, so we can compare the numbers. 7 is more than 5. "
                   "<b>Jug A</b> holds more."))
    order = [0, 1, 2, 3, 9, 10, 4, 5, 6, 7, 8, 11, 12, 13, 14, 15, 16, 17, 18, 19]
    assert sorted(order) == list(range(len(its)))
    its = [its[i] for i in order]
    assert len(its) == 20, len(its)
    return {"title": "Capacity with cups and jugs", "items": its}


# ============================================================ set 5: compare, order and word problems
def diff_e(a, b, d):
    e = "Take away the smaller number from the bigger one: %d − %d = <b>%d</b>. " % (a, b, d)
    if 2 <= d <= 5:
        e += "Or count on from %d to %d: %s. That is %d more. " % (b, a, count_list(d, b + 1), d)
    e += "Do not add: %d + %d = %d is both together." % (a, b, a + b)
    return e


def set_problems(P):
    its = []
    for A, a, B, b, ask in [("pencil", 11, "crayon", 6, "longer"), ("ribbon", 13, "straw", 9, "shorter")]:
        d = a - b
        q = fig(measure2_svg([(A, a), (B, b)], "cube"))
        if ask == "longer":
            q += "How many cubes longer is the %s than the %s?" % (A, B)
        else:
            q += "How many cubes shorter is the %s than the %s?" % (B, A)
        e = "The %s is %d cubes long. The %s is %d cubes long. " % (A, a, B, b) + diff_e(a, b, d)
        its.append(mcq_len(q, d, "cube", [a + b, d + 1, d - 1, a], e))

    a, b = P.next(), P.next()
    its.append(mcq_len("At the athletics carnival, %s jumps 9 footsteps. %s jumps 12 footsteps. "
                       "Their teacher measures both jumps with her footsteps. How much further does %s jump?" % (a[0], b[0], b[0]),
                       3, "step", [21, 4, 2], diff_e(12, 9, 3)))
    nm, he, his = P.next()
    its.append(mcq("Mum measures the classroom. It is 10 footsteps long. %s measures it too. %s gets 14 footsteps. Why?"
                   % (nm, cap(he)), "%s’s feet are smaller." % nm,
                   ["%s’s feet are bigger." % nm, "The room got longer.", "Mum counted wrong."],
                   "Smaller feet need more steps to cover the same room. So %s gets the bigger number. "
                   "<b>%s’s feet are smaller</b>." % (nm, nm)))
    nm, he, his = P.next()
    its.append(mcq("%s’s desk is 6 of %s handspans long. The teacher’s desk is 6 of the teacher’s handspans long. "
                   "Which desk is longer?" % (nm, his), "the teacher’s desk",
                   ["%s’s desk" % nm, "They are the same.", "You cannot tell."],
                   "Both are 6 handspans, but the teacher’s hand is bigger. So <b>the teacher’s desk</b> is longer. "
                   "The units are not the same size."))
    lists = [["blue", "green", "red"], ["red", "green", "blue"], ["green", "blue", "red"], ["blue", "red", "green"]]
    L = {"red": 15, "blue": 9, "green": 12}
    vs = [[L[c] for c in l] for l in lists]
    assert vs[0] == sorted(vs[0]) and all(v != sorted(v) for v in vs[1:])
    its.append(mcq("The red ribbon is 15 cubes long. The blue ribbon is 9 cubes. The green ribbon is 12 cubes. "
                   "Which order goes from shortest to longest?", ", ".join(lists[0]), [", ".join(l) for l in lists[1:]],
                   "9 is the smallest and 15 is the biggest. So the order is blue (9), green (12), <b>red (15)</b>."))
    its.append(mcq_len("A toy wombat balances 14 cubes. A toy koala balances 9 cubes. How many cubes heavier is the wombat?",
                       5, "cube", [23, 6, 4], diff_e(14, 9, 5)))
    nm, he, his = P.next()
    q = fig(balance_svg(("lunch box", 0), ("cubes", 11), "L", labels=["lunch box", "11 cubes"]))
    its.append(mcq_len(q + "%s needs 15 cubes to balance %s lunch box. %s has put on 11 cubes. How many more cubes does %s need?"
                       % (nm, his, cap(he), he), 4, "cube", [26, 11, 3],
                       "The lunch box side is still down, so more cubes are needed. Count on from 11 to 15: 12, 13, 14, 15. "
                       "That is 4. Or 15 − 11 = <b>4</b>. Check: 11 + 4 = 15."))
    nm, he, his = P.next()
    its.append(mcq("A bucket holds 9 cups of water. %s pours in 4 cups. How many more cups will fill it?" % nm,
                   "5 cups", ["13 cups", "4 cups", "6 cups"], diff_e(9, 4, 5)))
    nm, he, his = P.next()
    its.append(mcq("A watering can holds 8 cups. %s fills it 2 times to water the garden. How many cups of water is that?" % nm,
                   "16 cups", ["10 cups", "8 cups", "6 cups"],
                   "2 lots of 8 is double 8. 8 + 8 = <b>16</b>. Do not add 8 + 2."))
    its.append(mcq_len("A paper clip is as long as 2 cubes. A ruler is 7 paper clips long. How many cubes long is the ruler?",
                       14, "cube", [9, 7, 5],
                       "Each paper clip is 2 cubes. Count in 2s, 7 times: 2, 4, 6, 8, 10, 12, 14. "
                       "The ruler is <b>14 cubes</b> long."))
    nm, he, his = P.next()
    its.append(mcq_len("%s lays 3 craft sticks end to end along %s book. Each craft stick is 5 cubes long. "
                       "How many cubes long is the book?" % (nm, his), 15, "cube", [8, 5, 3],
                       "Count in 5s, 3 times: 5, 10, 15. The book is <b>15 cubes</b> long. Do not add 5 + 3."))
    nm, he, his = P.next()
    its.append(mcq("A jug at the school canteen holds 10 cups. %s pours out half. How many cups are left in the jug?" % nm,
                   "5 cups", ["20 cups", "10 cups", "8 cups"],
                   "Half means 2 equal parts. 5 + 5 = 10, so half of 10 is <b>5</b>. 20 would be double."))
    its.append(mcq("A toy kangaroo balances 7 cubes. A toy kookaburra balances 7 cubes. Which is true?", "They weigh the same.",
                   ["The kangaroo is heavier.", "The kookaburra is heavier.", "You cannot tell."],
                   "Both balance the same number of the same cubes. So <b>they weigh the same</b>."))
    a, b = P.next(), P.next()
    its.append(mcq_len("%s’s tower is 16 cubes tall. %s’s tower is 7 cubes shorter. How tall is %s’s tower?"
                       % (a[0], b[0], b[0]), 9, "cube", [23, 7, 10],
                       "“7 cubes shorter” means take away 7. 16 − 7 = <b>9</b>. Shorter, so the number must be "
                       "smaller than 16."))
    nm, he, his = P.next()
    its.append(mcq_len("A ribbon is 20 cubes long. %s cuts it in half. How long is each piece?" % nm, 10, "cube", [40, 18, 5],
                       "Half means 2 equal pieces. 10 + 10 = 20, so each piece is <b>10 cubes</b> long. Double would be 40."))
    a, b = P.next(), P.next()
    its.append(mcq("%s fills a bucket with 10 small cups. %s fills the same bucket with 5 big cups. Which is true?" % (a[0], b[0]),
                   "The bucket holds the same water.",
                   ["%s’s bucket holds more." % a[0], "%s’s bucket holds less." % a[0], "Big cups hold less."],
                   "It is the same bucket, so it holds the same water. 10 is more than 5 only because the cups "
                   "were smaller. <b>The bucket holds the same water</b>."))
    its.append(mcq_len("A path at the beach is 40 footsteps long. A slide is 25 footsteps long. The same child measured both. "
                       "How much longer is the path?", 15, "step", [65, 25, 16, 14], diff_e(40, 25, 15)))
    nm, he, his = P.next()
    its.append(mcq("%s’s shoe is 9 cubes long. %s’s mum’s shoe is 14 cubes long. How much longer is Mum’s shoe?"
                   % (nm, nm), "5 cubes", ["23 cubes", "14 cubes", "6 cubes"], diff_e(14, 9, 5)))
    nm, he, his = P.next()
    its.append(mcq("%s measures the sandpit: 12 big steps. Then %s uses small steps. Which could be right?" % (nm, he),
                   "18 small steps", ["12 small steps", "8 small steps", "6 small steps"],
                   "Small steps are shorter, so you need more of them than 12. Only <b>18 small steps</b> is more "
                   "than 12. A smaller unit gives a bigger number."))
    order = [0, 1, 5, 2, 3, 4, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19]
    assert sorted(order) == list(range(len(its)))
    its = [its[i] for i in order]
    assert len(its) == 20, len(its)
    return {"title": "Compare, order and solve word problems", "items": its}


# ============================================================ lesson
def body_html():
    return (
        "<h2>Measure with units that are all the same</h2>"
        "<p>To measure length, lay units <b>end to end</b> along the object. Start right at one end. "
        "Stop at the other end. No gaps and no overlaps. Then count the units.</p>"
        "<figure class='sn-fig'>" + measure_svg("crayon", 6, "cube") +
        "<figcaption>6 cubes fit from one end of the crayon to the other. The crayon is 6 cubes long.</figcaption></figure>"
        "<p>All the units must be the <b>same size</b>. Do not mix paper clips and cubes in one row, "
        "and do not use hands or feet of different sizes.</p>"
        "<h2>Bigger units, smaller units</h2>"
        "<p>A paper clip is as long as 2 cubes. The same crayon is 6 cubes or 3 paper clips. "
        "Both are right. A <b>smaller unit gives a bigger number</b>.</p>"
        "<figure class='sn-fig'>" + two_units_svg("crayon", 6) +
        "<figcaption>The crayon is 6 cubes long. It is also 3 paper clips long.</figcaption></figure>"
        "<p>If the units do not fit exactly, say “between”. Then use <b>smaller units</b> to measure more exactly.</p>"
        "<figure class='sn-fig'>" + about_svg("pencil", 7) +
        "<figcaption>The pencil is between 3 and 4 paper clips long. With cubes it is exactly 7 cubes.</figcaption></figure>"
        "<h2>Mass: heavier and lighter</h2>"
        "<p>Put two things on a balance. The <b>heavier</b> side goes down. The <b>lighter</b> side goes up. "
        "To measure mass, add cubes until the balance is level. Then count the cubes.</p>"
        "<figure class='sn-fig'>" + balance_svg(("apple", 0), ("cubes", 8), "=", labels=["apple", ""]) +
        "<figcaption>The scale is level. The apple has the same mass as 8 cubes.</figcaption></figure>"
        "<figure class='sn-fig'>" + balance_svg(("beach ball", 0), ("stone", 0), "R") +
        "<figcaption>The stone side is down, so the stone is heavier. The beach ball is bigger, but it is lighter.</figcaption></figure>"
        "<h2>Capacity: how much it holds</h2>"
        "<p>Fill a cup to the top and pour it into the container. Keep going until it is full. "
        "Count the cups. Use the same cup every time.</p>"
        "<figure class='sn-fig'>" + cups_jug_svg(7) +
        "<figcaption>7 full cups fill the jug. The jug holds 7 cups.</figcaption></figure>"
        + ex("Which holds more?", "Jug A holds 7 cups. Bottle B holds 5 cups. Both use the same cup.",
             "Same cup, so compare the numbers. 7 is more than 5.", "Jug A")
        + ex("How many longer?", "A pencil is 11 cubes long. A crayon is 6 cubes long. How many cubes longer is the pencil?",
             "11 − 6 = 5. Or count on from 6: 7, 8, 9, 10, 11. That is 5.", "5 cubes")
        + "<h2>Common mistakes</h2>"
        + table(["Mistake", "What to do instead"], [
            ["Leaving gaps between units", "Push the units together so they touch"],
            ["Overlapping the units", "Lay them end to end, not on top of each other"],
            ["Starting past the end", "Put the first unit right at one end"],
            ["Mixing units of different sizes", "Use only cubes or only paper clips"],
            ["Thinking a bigger unit gives a bigger number", "Smaller units give a bigger number"],
            ["Thinking bigger means heavier", "Use a balance: the side that goes down is heavier"],
            ["Thinking taller always holds more", "Fill one and pour it into the other"],
        ])
    )


FAQ = [
    {"q": "What measurement do Year 2 students learn in the Australian Curriculum?",
     "a": "Year 2 students measure and compare length, mass and capacity with uniform informal units, such as cubes, "
          "paper clips and cups, and use smaller units when they need to be more accurate."},
    {"q": "What are informal units of measurement?",
     "a": "Informal units are everyday objects used to measure, such as cubes, paper clips, handspans, footsteps or cups. "
          "In Year 2 they must all be the same size, so everyone gets the same answer."},
    {"q": "Why do Year 2 students use informal units instead of a ruler?",
     "a": "Laying units end to end shows what measuring means: counting how many same-size units fit. "
          "This makes centimetres, grams and litres easy to understand in Year 3."},
    {"q": "How can I help my child practise measuring at home?",
     "a": "Measure things with Lego bricks, paper clips or a cup: a book, a shoe, a saucepan. "
          "Ask “Which is longer, heavier or holds more?” and check there are no gaps between the units."},
]


def gen():
    rnd = random.Random(2812)
    P = People(rnd)
    sets = [set_units(P), set_choose(P), set_mass(P), set_capacity(P), set_problems(P)]
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
                assert not re.search(r"\b1 (cubes|paper clips|cups|footsteps)\b", c), c
                assert not re.search(r"\b([02-9]|\d\d+) (cube|paper clip|cup|footstep)\b", c), c
    # pictures: the answer is the number of units shown
    n = 0
    for s in sets:
        for it in s["items"]:
            m = re.search(r"aria-label='([a-z -]+) (\d+) (cubes|paper clips) long, above (\d+)", it["q"])
            if m:
                unit = "cube" if m.group(3) == "cubes" else "clip"
                assert it["c"][it["a"]] == u(int(m.group(2)), unit)
                n += 1
            m = re.search(r"aria-label='balance scale with ([a-z ]+) on the left and (\d+) cubes on the right, the two sides are level", it["q"])
            if m and "How many cubes balance" in it["q"]:
                assert it["c"][it["a"]] == "%s cubes" % m.group(2)
                n += 1
            m = re.search(r"aria-label='an empty (jug|bucket) and (\d+) cups", it["q"])
            if m and "How many cups does" in it["q"]:
                assert it["c"][it["a"]] == "%s cups" % m.group(2)
                n += 1
            m = re.search(r"aria-label='([a-z ]+) measured with (\d+) cubes and with (\d+) paper clips", it["q"])
            if m:
                want = m.group(3) + " paper clips" if "How many paper clips" in it["q"] else m.group(2) + " cubes"
                assert it["c"][it["a"]] == want, (it["c"], want)
                n += 1
            m = re.search(r"aria-label='([a-z ]+) between (\d+) and (\d+) paper clips long", it["q"])
            if m and "How long" in it["q"]:
                assert it["c"][it["a"]] == "between %s and %s paper clips" % (m.group(2), m.group(3))
                n += 1
    assert n == 12 + 5 + 4 + 5 + 3, n
    # heavier/lighter pictures: the answer names the object on the side that is down (or up)
    for it in sets[2]["items"]:
        m = re.search(r"with ([a-z ]+) on the left and ([a-z ]+) on the right, the (left|right) side is down'", it["q"])
        if m and "Which is heavier" in it["q"]:
            assert it["c"][it["a"]] == "the " + (m.group(1) if m.group(3) == "left" else m.group(2))
        if m and "Which is lighter" in it["q"]:
            assert it["c"][it["a"]] == "the " + (m.group(2) if m.group(3) == "left" else m.group(1))
    # A-D pictures
    for it in sets[3]["items"]:
        m = re.search(r"glasses of the same size: ([^']+)'", it["q"])
        if m:
            st = dict(x.split(" ", 1) for x in m.group(1).split(", "))
            ans = "ABCD"[it["a"]]
            if "half full?" in it["q"]:
                assert st[ans] == "half full" and list(st.values()).count("half full") == 1
                continue
            f = max if "most" in it["q"] else min
            assert LEVEL[st[ans]] == f(LEVEL[v] for v in st.values())
            assert [LEVEL[v] for v in st.values()].count(LEVEL[st[ans]]) == 1
        m = re.search(r"full containers of different sizes: ([^']+)'", it["q"])
        if m:
            dims = [tuple(map(int, re.findall(r"\d+", x))) for x in m.group(1).split(", ")]
            areas = [w * h for w, h in dims]
            i = it["a"]
            if "most" in it["q"]:
                assert areas[i] == max(areas) and dims[i][0] == max(d[0] for d in dims) and dims[i][1] == max(d[1] for d in dims)
            else:
                assert areas[i] == min(areas) and dims[i][0] == min(d[0] for d in dims) and dims[i][1] == min(d[1] for d in dims)
    return {
        "country": "au", "subject": "maths", "grade": "year-2", "slug": "measuring-length-mass-and-capacity", "sort": 12,
        "updated": UPDATED, "pdf_url": "",
        "title": "Measuring Length, Mass and Capacity",
        "seo_title": "Year 2 Measuring Worksheets: Length, Mass and Capacity with Informal Units (Free, with Answer Key)",
        "short_title": "Measuring length, mass and capacity",
        "domain": "Measurement",
        "standard_code": "AC9M2M01",
        "standard_url": "https://v9.australiancurriculum.edu.au/f-10-curriculum/learning-areas/mathematics",
        "standard_text": "Measure and compare objects based on length, capacity and mass using appropriate uniform "
                         "informal units and smaller units for accuracy when necessary",
        "meta_desc": "Free Year 2 maths worksheets on measuring with informal units: length with cubes and paper clips, "
                     "choosing same-size and smaller units, mass on a balance, capacity with cups and jugs, and "
                     "word problems. 100 picture questions with an answer key, matched to the Australian Curriculum.",
        "key_big": "Lay same-size units end to end with no gaps, then count them.",
        "key_sub": "A smaller unit gives a bigger number. On a balance the heavier side goes down, and bigger is not "
                   "always heavier.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }


if __name__ == "__main__":
    out = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, out["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(out, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
