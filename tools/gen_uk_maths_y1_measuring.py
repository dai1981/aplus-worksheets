# -*- coding: utf-8 -*-
"""
UK Year 1 Maths: Length, Height, Mass and Capacity (National Curriculum in England, Year 1: Measurement)
  python tools/gen_uk_maths_y1_measuring.py
Compare and measure with non-standard units (cubes, paper clips, cups); cm, kg and litres only lightly.
Every picture is drawn exactly from the data: objects run from one cube boundary to another, the heavier
side of a balance is the lower one, and water levels are exact fractions of a straight-sided container.
Wrong answers come from real mistakes: not lining up the ends (starting at the wrong end), counting the
lines between cubes, counting cubes past the end, thinking bigger means heavier, and mixing up half full
with nearly full or quarter full.
HTML attributes use single quotes (no backslashes in the JSON).
"""
import json, os, random, re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "uk", "maths", "year-1")
UPDATED = "2026-11-02"
GREEN = "#006633"
INK = "#2b2b2b"
GREY = "#8a8a8a"
WATER = "#9fd3f2"
WATER_LINE = "#2a7fb8"
FONT = "Arial, Helvetica, sans-serif"
GIRLS = ["Amelia", "Isla", "Freya", "Poppy", "Ava", "Aisha", "Lily", "Zara", "Grace", "Ruby", "Maya", "Evie"]
BOYS = ["Oliver", "Harry", "Mohammed", "Jack", "Arjun", "Noah", "George", "Leo", "Alfie", "Kai", "Ethan", "Charlie"]

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
    elif kind == "lolly stick":
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
    elif kind == "felt-tip pen":
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
    elif kind == "melon":
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


# ============================================================ set 1: longer, shorter, taller
def set_compare(P):
    its = []
    OTHER = ["They are the same.", "You cannot tell."]

    def two(objs, ask, picture, up=False):
        (a, la), (b, lb) = objs
        names = [the(a), the(b)]
        if la == lb:
            e = "Both start at the same line. Both end at the same place. They are <b>the same length</b>."
            return mcq(fig(picture) + "Which is %s?" % ask, "They are the same.", names + ["You cannot tell."], e)
        big, small = (a, b) if la > lb else (b, a)
        win = big if ask in ("longer", "taller") else small
        lose = small if win == big else big
        if not up:
            e = ("Both start at the same line. Look at the other end. The %s goes further, so it is longer. "
                 "The <b>%s is %s</b>." % (big, win, ask))
        else:
            e = ("Both stand on the floor. Look at the tops. The %s reaches higher, so it is taller. "
                 "The <b>%s is %s</b>." % (big, win, ask))
        return mcq(fig(picture) + "Which is %s?" % ask, the(win), [the(lose)] + OTHER, e)

    for objs, ask in [((("pencil", 9), ("crayon", 5)), "longer"), ((("ribbon", 6), ("straw", 10)), "longer"),
                      ((("nail", 5), ("pencil", 8)), "shorter"), ((("key", 3), ("felt-tip pen", 7)), "longer"),
                      ((("strip of paper", 11), ("crayon", 6)), "shorter"), ((("rubber", 3), ("ribbon", 7)), "shorter")]:
        its.append(two(objs, ask, compare_svg([(k, 0, L) for k, L in objs])))
    its.append(two((("crayon", 6), ("key", 6)), "longer", compare_svg([("crayon", 0, 6), ("key", 0, 6)])))
    its.append(two((("lolly stick", 8), ("leaf", 4)), "longer", compare_svg([("lolly stick", 0, 8), ("leaf", 0, 4)])))

    for objs, ask in [((("pencil", 8), ("crayon", 5)), "taller"), ((("felt-tip pen", 6), ("straw", 9)), "taller"),
                      ((("lolly stick", 7), ("crayon", 4)), "shorter")]:
        its.append(two(objs, ask, tall_svg(list(objs)), up=True))

    for objs, ask in [((("straw", 10), ("key", 3), ("pencil", 7)), "longest"),
                      ((("crayon", 5), ("ribbon", 9), ("rubber", 3)), "shortest"),
                      ((("felt-tip pen", 6), ("strip of paper", 11), ("leaf", 4)), "longest")]:
        lens = [L for _, L in objs]
        names = [k for k, _ in objs]
        best = names[lens.index(max(lens) if ask == "longest" else min(lens))]
        mid = sorted(objs, key=lambda t: t[1])[1][0]
        q = fig(compare_svg([(k, 0, L) for k, L in objs])) + "Which is the %s?" % ask
        e = ("All three start at the same line. Look at where each one ends. The <b>%s</b> is the %s. "
             "The %s is in the middle." % (best, ask, mid))
        its.append(mcq(q, the(best), [the(n) for n in names if n != best] + ["They are the same."], e))

    for (a, la), (b, sb, lb) in [(("pencil", 7), ("crayon", 4, 5)), (("ribbon", 8), ("straw", 5, 6)),
                                 (("felt-tip pen", 7), ("lolly stick", 5, 4))]:
        assert la > lb and sb + lb > la
        q = fig(compare_svg([(a, 0, la), (b, sb, lb)], line=False)) + "They do not start at the same place. Which is longer?"
        e = ("The %s ends further along, but it starts later. Slide it back so the ends line up. "
             "Then the %s sticks out past it. The <b>%s is longer</b>." % (b, a, a))
        its.append(mcq(q, the(a), [the(b)] + OTHER, e))

    its.append(mcq("You want to find the longer pencil. What do you do first?", "Line up the ends.",
                   ["Look at the colours.", "Count the pencils.", "Look at the tips only."],
                   "Put the pencils side by side. <b>Line up one end</b>. Then look at the other end. "
                   "The one that sticks out is longer."))
    its.append(mcq("A rope is longer than a stick. Which is true?", "The stick is shorter.",
                   ["The stick is longer.", "The rope is shorter.", "They are the same."],
                   "The rope is longer than the stick. So the stick is <b>shorter</b> than the rope. "
                   "It is the same fact said the other way."))
    a = P.next()
    m = P.next()
    its.append(mcq("%s and %s stand back to back. %s’s head is higher. Who is taller?" % (a[0], m[0], a[0]), a[0],
                   [m[0], "They are the same.", "You cannot tell."],
                   "Their feet are on the same floor. The higher head belongs to the taller child. "
                   "<b>%s is taller</b>." % a[0]))
    assert len(its) == 20, len(its)
    return {"title": "Longer, shorter and taller", "items": its}


# ============================================================ set 2: measure with cubes and paper clips
S2 = [("crayon", 4, "cube", None), ("key", 3, "cube", None), ("pencil", 7, "cube", None),
      ("rubber", 2, "clip", None), ("ribbon", 5, "cube", None), ("leaf", 3, "clip", None),
      ("straw", 9, "cube", None), ("felt-tip pen", 4, "clip", None), ("caterpillar", 6, "cube", None),
      ("strip of paper", 5, "clip", None), ("lolly stick", 8, "cube", None),
      ("nail", 5, "cube", 8), ("worm", 7, "cube", 10)]

OK = "Yes, it is right."
GAP = "No, there are gaps."
OVER = "No, they overlap."
START = "No, the start is wrong."
MODE_ANS = {"exact": OK, "gap": GAP, "overlap": OVER, "late": START}


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

    its.append(mcq("You measure a crayon with cubes. What do you count?", "the cubes under it",
                   ["all the cubes in the box", "the lines between cubes", "the colours of the cubes"],
                   "Lay cubes along the crayon from end to end. Count only <b>the cubes under the crayon</b>. "
                   "That number is its length."))
    its.append(mcq("Where should you put the first cube?", "at one end",
                   ["in the middle", "a little past the end", "anywhere"],
                   "Put the first cube right <b>at one end</b>. Then lay the next cubes end to end until you reach the other end."))

    for kind, L, unit, mode in [("pencil", 7, "cube", "exact"), ("crayon", 4, "clip", "gap"),
                                ("ribbon", 7, "clip", "overlap"), ("straw", 6, "cube", "late")]:
        q = fig(wrong_svg(kind, L, unit, mode)) + "Is this the right way to measure the %s?" % kind
        un = UNAME[unit][1]
        if mode == "exact":
            e = ("Yes. The %s start at one end of the %s and go to the other end. They touch with no gaps. "
                 "The %s is <b>%s</b> long." % (un, kind, kind, u(L, unit)))
        elif mode == "gap":
            e = ("<b>No, there are gaps</b> between the %s. The gaps are not counted, so the number is too small. "
                 "Push the %s together so they touch." % (un, un))
        elif mode == "overlap":
            e = "<b>No, the %s overlap</b>. Some lie on top of others, so you count too many. Lay them end to end." % un
        else:
            e = ("<b>No, the start is wrong.</b> The first %s does not start at the end of the %s. "
                 "Line up the first one with the end of the %s." % (UNAME[unit][0], kind, kind))
        its.append(mcq(q, MODE_ANS[mode], [x for x in [OK, GAP, OVER, START] if x != MODE_ANS[mode]], e))

    q = fig(two_units_svg("crayon", 6)) + "The crayon is 6 cubes long. How many paper clips long is it?"
    its.append(mcq_len(q, 3, "clip", [6, 12, 4],
                       "Look at the bottom row. Count the paper clips under the crayon: 1, 2, 3. It is <b>3 paper clips</b> long. "
                       "A paper clip is longer than a cube, so you need fewer."))
    order = [0, 1, 2, 3, 4, 13, 5, 6, 7, 8, 14, 9, 10, 15, 16, 11, 12, 17, 18, 19]
    its = [its[i] for i in order]
    assert len(its) == 20, len(its)
    return {"title": "Measure with cubes and paper clips", "items": its}


# ============================================================ set 3: heavier and lighter
def set_mass(P):
    its = []
    SAME = "They weigh the same."
    CANT = "You cannot tell."

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
            e += " The %s looks bigger, but bigger is not always heavier." % ("beach ball" if "beach ball" in (a, b) else "pillow")
        return mcq(q, the(win), [the(lose), SAME, CANT], e)

    its.append(pair("book", "feather", "L", "heavier"))
    its.append(pair("orange", "melon", "R", "heavier"))
    its.append(pair("brick", "sponge", "L", "lighter"))
    its.append(pair("egg", "shoe", "R", "lighter"))
    for a, b in [("apple", "orange"), ("pear", "banana")]:
        q = fig(balance_svg((a, 0), (b, 0), "=")) + "The scale is level. Which is true?"
        e = "The two sides are level. Neither side goes down. So <b>they weigh the same</b>."
        its.append(mcq(q, SAME, ["The %s is heavier." % a, "The %s is heavier." % b, CANT], e))
    its.append(pair("beach ball", "stone", "R", "heavier", trap=True))
    its.append(pair("pillow", "tin of beans", "R", "heavier", trap=True))
    its.append(pair("teddy", "brick", "R", "lighter"))
    its.append(pair("toy car", "feather", "L", "lighter"))

    for kind, n in [("apple", 6), ("banana", 5), ("toy car", 9), ("teddy", 11)]:
        q = fig(balance_svg((kind, 0), ("cubes", n), "=", labels=[kind, ""])) + "The scale is level. How many cubes balance the %s?" % kind
        e = ("The scale is level, so the cubes weigh the same as the %s. Count the cubes: %s. "
             "<b>%d cubes</b> balance the %s." % (kind, count_list(n), n, kind))
        its.append(mcq_len(q, n, "cube", [n + 1, n - 1, n + 2], e))

    q = fig(balance_svg(("orange", 0), ("cubes", 4), "L", labels=["orange", "4 cubes"])) + "Which is true?"
    its.append(mcq(q, "The orange is heavier than 4 cubes.",
                   ["The orange is lighter than 4 cubes.", "The orange weighs the same as 4 cubes.", CANT],
                   "The orange side goes down. The side that goes down is heavier. So <b>the orange is heavier than 4 cubes</b>."))
    q = fig(balance_svg(("feather", 0), ("cubes", 2), "R", labels=["feather", "2 cubes"])) + "Which is true?"
    its.append(mcq(q, "The feather is lighter than 2 cubes.",
                   ["The feather is heavier than 2 cubes.", "The feather weighs the same as 2 cubes.", CANT],
                   "The feather side goes up. The side that goes up is lighter. So <b>the feather is lighter than 2 cubes</b>."))

    its.append(mcq("A brick and a sponge are on a balance. The brick is heavier. Which side goes down?",
                   "the brick side", ["the sponge side", "Both go down.", "Neither side."],
                   "The heavier thing makes its side go down. The brick is heavier, so <b>the brick side</b> goes down."))
    nm, he, his = P.next()
    its.append(mcq("%s thinks the beach ball is heavier because it is bigger. On the balance, the beach ball side goes up. "
                   "Is %s right?" % (nm, nm),
                   "No, the ball is lighter.", ["Yes, the ball is heavier.", SAME, CANT],
                   "The side that goes up is lighter. So the beach ball is lighter. "
                   "<b>%s is not right</b>. Big things can be light." % nm))
    its.append(mcq("The melon is heavier than the apple. The apple is heavier than the grape. Which is the lightest?",
                   "the grape", ["the melon", "the apple", CANT],
                   "From heaviest to lightest: melon, apple, grape. <b>The grape</b> is the lightest."))
    its.append(mcq("The tin is lighter than the bag. The bag is lighter than the box. Which is the heaviest?",
                   "the box", ["the tin", "the bag", CANT],
                   "Each one is lighter than the next. From lightest: tin, bag, box. So <b>the box</b> is the heaviest. "
                   "Read “lighter” carefully."))
    assert len(its) == 20, len(its)
    return {"title": "Heavier and lighter on a balance", "items": its}


# ============================================================ set 4: full, empty, half full, quarter full
STATE_DIST = {"full": ["nearly full", "half full", "empty"],
              "empty": ["nearly empty", "quarter full", "full"],
              "half full": ["nearly full", "quarter full", "full"],
              "quarter full": ["half full", "empty", "full"],
              "nearly full": ["full", "half full", "nearly empty"],
              "nearly empty": ["empty", "half full", "full"]}
STATE_E = {"full": "The water comes right up to the top. The %s is <b>full</b>.",
           "empty": "There is no water at all. The %s is <b>empty</b>.",
           "half full": "The water comes up to the middle. Half is water and half is empty. The %s is <b>half full</b>, not nearly full.",
           "quarter full": "Split the %s into 4 equal parts. The water fills 1 part. It is <b>quarter full</b>. Half full would reach the middle.",
           "nearly full": "The water is close to the top, but not right at the top. The %s is <b>nearly full</b>.",
           "nearly empty": "There is only a little water at the bottom. The %s is <b>nearly empty</b>."}


def set_capacity(P):
    its = []
    for state, kind, dist in [("full", "glass", None), ("empty", "glass", None), ("half full", "glass", None),
                              ("quarter full", "glass", None), ("nearly full", "jar", None),
                              ("half full", "jar", ["nearly full", "quarter full", "empty"]),
                              ("nearly empty", "jar", None),
                              ("quarter full", "jar", ["half full", "nearly full", "empty"])]:
        q = fig(glass_svg(state, kind)) + "How full is the %s?" % kind
        e = STATE_E[state] % kind if "%s" in STATE_E[state] else STATE_E[state]
        its.append(mcq(q, state, dist or STATE_DIST[state], e))

    ABCD = ["A", "B", "C", "D"]
    for states, ask, ans, e in [
        (["half full", "nearly full", "quarter full", "empty"], "Which glass has the most water?", "B",
         "The glasses are the same size. Look for the highest water. Glass B is nearly full, so <b>B</b> has the most."),
        (["full", "half full", "nearly empty", "quarter full"], "Which glass has the least water?", "C",
         "Look for the lowest water. Glass C is nearly empty. It has less than D, which is quarter full. "
         "So <b>C</b> has the least."),
        (["quarter full", "full", "nearly full", "half full"], "Which glass is half full?", "D",
         "Half full means the water comes up to the middle. Glass C is nearly full, not half full. <b>D</b> is half full."),
        (["quarter full", "half full", "empty", "nearly full"], "Which glass is quarter full?", "A",
         "Quarter full means 1 of 4 equal parts has water. Glass B is half full. <b>A</b> is quarter full."),
        (["nearly full", "full", "half full", "quarter full"], "Which glass is full?", "B",
         "Full means the water comes right up to the top. A is nearly full, but there is a gap at the top. <b>B</b> is full."),
    ]:
        its.append(mcq(fig(glasses_svg(states)) + ask, ans, ABCD, e, lock=True))

    its.append(mcq(fig(sizes_svg([(34, 60), (70, 90), (24, 90), (50, 40)])) +
                   "Each container is full. Which one holds the most?", "B", ABCD,
                   "B is the widest and as tall as C. C is tall but very thin. So <b>B</b> holds the most. "
                   "Tall does not always mean it holds more.", lock=True))
    its.append(mcq(fig(sizes_svg([(40, 70), (60, 50), (24, 30), (34, 90)])) +
                   "Each container is full. Which one holds the least?", "C", ABCD,
                   "C is the thinnest and the shortest. So <b>C</b> holds the least.", lock=True))

    for n in (4, 7):
        nm, he, his = P.next()
        q = fig(cups_jug_svg(n)) + "%s pours all the cups into the jug. Now the jug is full. How many cups does the jug hold?" % nm
        e = "Count the cups: %s. The jug holds <b>%d cups</b> of water. Do not count the jug." % (count_list(n), n)
        its.append(mcq(q, "%d cups" % n, ["%d cups" % (n + 1), "%d cups" % (n - 1), "%d cups" % (n + 2)], e))

    its.append(mcq("Which can hold more water?", "a bucket", ["a cup", "They hold the same.", "a spoon"],
                   "A bucket is much bigger inside than a cup or a spoon. <b>A bucket</b> holds more."))
    nm, he, his = P.next()
    its.append(mcq("%s’s cup of milk is full. %s drinks half of it. How full is the cup now?" % (nm, cap(he)),
                   "half full", ["nearly full", "empty", "quarter full"],
                   "Half the milk is gone. Half is left. The cup is <b>half full</b>."))
    nm, he, his = P.next()
    its.append(mcq("A glass is half full. %s adds water until it is full. Is there more or less water now?" % nm,
                   "more water", ["less water", "the same amount","no water"],
                   "The water went up from the middle to the top. So there is <b>more water</b> now."))
    order = [0, 1, 2, 3, 4, 5, 6, 7, 8, 13, 15, 9, 10, 18, 11, 12, 16, 14, 17, 19]
    its = [its[i] for i in order]
    assert len(its) == 20, len(its)
    return {"title": "Full, empty, half full and quarter full", "items": its}


# ============================================================ set 5: practical problems
def diff_e(a, b, d, un):
    e = "Take away the smaller number from the bigger one: %d − %d = <b>%d</b>. " % (a, b, d)
    if 2 <= d <= 5:
        e += "Or count on from %d to %d: %s. That is %d more. " % (b, a, count_list(d, b + 1), d)
    e += "Do not add: %d + %d = %d is both together." % (a, b, a + b)
    return e


def set_problems(P):
    its = []
    for A, a, B, b, ask in [("pencil", 9, "crayon", 5, "longer"), ("ribbon", 10, "rubber", 3, "longer"),
                            ("felt-tip pen", 7, "caterpillar", 4, "shorter"), ("straw", 12, "pencil", 8, "shorter")]:
        d = a - b
        q = fig(measure2_svg([(A, a), (B, b)], "cube"))
        if ask == "longer":
            q += "How many cubes longer is the %s than the %s?" % (A, B)
        else:
            q += "How many cubes shorter is the %s than the %s?" % (B, A)
        e = "The %s is %d cubes long. The %s is %d cubes long. " % (A, a, B, b) + diff_e(a, b, d, "cubes")
        its.append(mcq_len(q, d, "cube", [a + b, d + 1, d - 1, a], e))

    its.append(mcq("The red ribbon is 7 cubes long. The blue ribbon is 12 cubes long. The green ribbon is 9 cubes long. "
                   "Which ribbon is the longest?", "the blue ribbon", ["the red ribbon", "the green ribbon", "They are the same."],
                   "12 is the biggest number. So <b>the blue ribbon</b> is the longest."))
    its.append(mcq("Jug A holds 6 cups of water. Jug B holds 9 cups. Which jug holds more?", "jug B",
                   ["jug A", "They hold the same.", "You cannot tell."],
                   "9 cups is more than 6 cups. So <b>jug B</b> holds more."))
    its.append(mcq("An apple balances 6 cubes. A pear balances 8 cubes. Which is heavier?", "the pear",
                   ["the apple", "They weigh the same.", "You cannot tell."],
                   "The pear needs more cubes to balance. 8 is more than 6. So <b>the pear</b> is heavier."))
    its.append(mcq_len("A pear balances 8 cubes. An apple balances 5 cubes. How many cubes heavier is the pear?", 3, "cube",
                       [13, 4, 2], diff_e(8, 5, 3, "cubes")))
    a, b = P.next(), P.next()
    its.append(mcq_len("%s’s ribbon is 4 cubes long. %s’s ribbon is double that. How long is %s’s ribbon?" % (a[0], b[0], b[0]),
                       8, "cube", [6, 2, 4],
                       "Double means two lots of the same. 4 + 4 = <b>8</b>. %s’s ribbon is 8 cubes long." % b[0]))
    nm, he, his = P.next()
    its.append(mcq_len("A straw is 10 cubes long. %s cuts it in half. How long is each piece?" % nm, 5, "cube", [20, 8, 10],
                       "Half means 2 equal pieces. 5 + 5 = 10, so each piece is <b>5 cubes</b> long. Double would be 20."))
    nm, he, his = P.next()
    its.append(mcq("A jug holds 8 cups of water. %s pours out 3 cups. How many cups are left in the jug?" % nm,
                   "5 cups", ["11 cups", "4 cups", "6 cups"],
                   "Pouring out means take away. 8 − 3 = <b>5</b>. There are 5 cups left."))
    nm, he, his = P.next()
    its.append(mcq("A glass is half full. %s drinks half of the water. How full is the glass now?" % nm,
                   "quarter full", ["half full", "empty", "nearly full"],
                   "Half full is 2 quarters. Drinking half of that leaves 1 quarter. The glass is <b>quarter full</b>."))
    its.append(mcq("Which would you use to find how heavy a bag of apples is?", "kilograms (kg)",
                   ["centimetres (cm)", "litres", "metres (m)"],
                   "We weigh things in <b>kilograms</b>. Centimetres and metres are for length. Litres are for water."))
    its.append(mcq("Which would you use to find how much water a bucket holds?", "litres",
                   ["kilograms (kg)", "centimetres (cm)", "metres (m)"],
                   "We measure how much a container holds in <b>litres</b>."))
    its.append(mcq("A pencil is 15 cm long. A crayon is 9 cm long. How much longer is the pencil?", "6 cm",
                   ["24 cm", "7 cm", "5 cm"], diff_e(15, 9, 6, "cm")))
    its.append(mcq("A bag of potatoes weighs 5 kg. A bag of carrots weighs 2 kg. How much heavier are the potatoes?", "3 kg",
                   ["7 kg", "2 kg", "4 kg"], diff_e(5, 2, 3, "kg")))
    its.append(mcq("A big bottle holds 2 litres. A small bottle holds 1 litre. How much do they hold together?", "3 litres",
                   ["1 litre", "2 litres", "4 litres"],
                   "Together means add. 2 + 1 = <b>3</b>. They hold 3 litres."))
    a, b = P.next(), P.next()
    its.append(mcq_len("%s’s tower is 9 cubes tall. %s’s tower is 4 cubes taller. How tall is %s’s tower?" % (a[0], b[0], b[0]),
                       13, "cube", [5, 9, 12],
                       "“4 cubes taller” means add 4. 9 + 4 = <b>13</b>. It is taller, so the number must be bigger than 9."))
    nm, he, his = P.next()
    its.append(mcq_len("%s needs 12 cubes to balance a book. %s has put 7 cubes on the scale. How many more cubes does %s need?"
                       % (nm, cap(he), he), 5, "cube", [19, 4, 6],
                       "Count on from 7 to 12: 8, 9, 10, 11, 12. That is 5. Or 12 − 7 = <b>5</b>. Check: 7 + 5 = 12."))
    nm, he, his = P.next()
    its.append(mcq("%s lines up 3 ribbons. The red one is longer than the blue one. The blue one is longer than the green one. "
                   "Which is the shortest?" % nm, "the green one", ["the red one", "the blue one", "You cannot tell."],
                   "From longest to shortest: red, blue, green. <b>The green one</b> is the shortest."))
    assert len(its) == 20, len(its)
    return {"title": "Measuring problems", "items": its}


# ============================================================ lesson
def body_html():
    return (
        "<h2>Longer, shorter and taller</h2>"
        "<p>Put two things side by side. Line up one end. Look at the other end. "
        "The one that sticks out is <b>longer</b>. The other is <b>shorter</b>. "
        "For things that stand up, we say <b>taller</b> and <b>shorter</b>.</p>"
        "<figure class='sn-fig'>" + compare_svg([("pencil", 0, 8), ("crayon", 0, 5)]) +
        "<figcaption>Both start at the same line. The pencil is longer. The crayon is shorter.</figcaption></figure>"
        "<h2>Measure with cubes</h2>"
        "<p>Lay cubes along the object, <b>end to end</b>. Start right at one end. Stop at the other end. "
        "Count the cubes. That number is the length.</p>"
        "<figure class='sn-fig'>" + measure_svg("crayon", 6, "cube") +
        "<figcaption>6 cubes fit from one end of the crayon to the other. The crayon is 6 cubes long.</figcaption></figure>"
        "<h2>Heavier and lighter</h2>"
        "<p>Put two things on a balance. The <b>heavier</b> side goes down. The <b>lighter</b> side goes up. "
        "If the sides are level, they weigh the same.</p>"
        "<figure class='sn-fig'>" + balance_svg(("beach ball", 0), ("stone", 0), "R") +
        "<figcaption>The stone side is down, so the stone is heavier. The beach ball is bigger, but it is lighter.</figcaption></figure>"
        "<figure class='sn-fig'>" + balance_svg(("apple", 0), ("cubes", 6), "=", labels=["apple", ""]) +
        "<figcaption>The scale is level. The apple weighs the same as 6 cubes.</figcaption></figure>"
        "<h2>Full, half full, quarter full, empty</h2>"
        "<p>Look at how high the water comes in the container.</p>"
        "<figure class='sn-fig'>" + glasses_svg(["full", "half full", "quarter full", "empty"],
                                               ["full", "half", "quarter", "empty"]) +
        "<figcaption>Full reaches the top. Half full reaches the middle. Quarter full fills 1 of 4 equal parts. Empty has no water.</figcaption></figure>"
        + ex("Which holds more?", "Jug A holds 6 cups of water. Jug B holds 9 cups. Which holds more?",
             "Count the cups each jug holds. 9 is more than 6.", "Jug B")
        + ex("How many longer?", "A pencil is 9 cubes long. A crayon is 5 cubes long. How many cubes longer is the pencil?",
             "9 − 5 = 4. Or count on from 5: 6, 7, 8, 9. That is 4.", "4 cubes")
        + "<h2>Common mistakes</h2>"
        + table(["Mistake", "What to do instead"], [
            ["Not lining up the ends", "Start both objects at the same line"],
            ["Starting the cubes past the end", "Put the first cube right at one end"],
            ["Counting the lines between cubes", "Count the cubes themselves"],
            ["Leaving gaps between cubes", "Push the cubes together so they touch"],
            ["Thinking bigger means heavier", "Use a balance: the side that goes down is heavier"],
            ["Calling nearly full “half full”", "Half full means the water reaches the middle"],
        ])
    )


FAQ = [
    {"q": "What measurement does a Year 1 child learn?",
     "a": "Year 1 pupils compare lengths and heights, mass and capacity using words like longer, taller, heavier, full and half full. "
          "They begin to measure with cubes, paper clips and cups, and meet cm, kg and litres."},
    {"q": "How do you teach heavier and lighter in Year 1?",
     "a": "Use a balance scale. The heavier side goes down and the lighter side goes up. "
          "Try a big light object and a small heavy one so children see that bigger is not always heavier."},
    {"q": "Why do Year 1 children measure with cubes instead of a ruler?",
     "a": "Laying cubes end to end shows what length is: how many same-size units fit along an object. "
          "This makes rulers and centimetres easy to understand in Year 2."},
    {"q": "What is the difference between half full and nearly full?",
     "a": "Half full means the water comes up to the middle of the container. Nearly full means it is close to the top."},
]


def gen():
    rnd = random.Random(1106)
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
                assert not re.search(r"\b1 (cubes|paper clips|cups)\b", c), c
                assert not re.search(r"\b([02-9]|\d\d+) (cube|paper clip|cup)\b", c), c
    # one-object pictures: the answer is the number of units under the object
    n = 0
    for s in sets:
        for it in s["items"]:
            m = re.search(r"aria-label='([a-z -]+) (\d+) (cubes|paper clips) long, above (\d+)", it["q"])
            if m:
                unit = "cube" if m.group(3) == "cubes" else "clip"
                assert it["c"][it["a"]] == u(int(m.group(2)), unit)
                n += 1
            m = re.search(r"aria-label='balance scale with ([a-z ]+) on the left and (\d+) cubes on the right, the two sides are level", it["q"])
            if m:
                assert it["c"][it["a"]] == "%s cubes" % m.group(2)
                n += 1
            m = re.search(r"aria-label='an empty jug and (\d+) cups", it["q"])
            if m:
                assert it["c"][it["a"]] == "%s cups" % m.group(1)
                n += 1
    assert n == 13 + 4 + 2, n
    # heavier/lighter pictures: the answer names the object on the side that is down (or up)
    for it in sets[2]["items"]:
        m = re.search(r"with ([a-z ]+) on the left and ([a-z ]+) on the right, the (left|right) side is down'", it["q"])
        if m and "Which is heavier" in it["q"]:
            assert it["c"][it["a"]] == "the " + (m.group(1) if m.group(3) == "left" else m.group(2))
        if m and "Which is lighter" in it["q"]:
            assert it["c"][it["a"]] == "the " + (m.group(2) if m.group(3) == "left" else m.group(1))
    # A-D glass pictures: the answer letter matches the asked state / extreme
    for it in sets[3]["items"]:
        m = re.search(r"glasses of the same size: ([^']+)'", it["q"])
        if m:
            st = dict(x.split(" ", 1) for x in m.group(1).split(", "))
            ans = "ABCD"[it["a"]]
            if "most" in it["q"]:
                assert LEVEL[st[ans]] == max(LEVEL[v] for v in st.values())
            elif "least" in it["q"]:
                assert LEVEL[st[ans]] == min(LEVEL[v] for v in st.values())
            else:
                want = re.search(r"Which glass is ([a-z ]+)\?", it["q"]).group(1)
                assert st[ans] == want and list(st.values()).count(want) == 1
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
        "country": "uk", "subject": "maths", "grade": "year-1", "slug": "length-height-mass-and-capacity", "sort": 6,
        "updated": UPDATED, "pdf_url": "",
        "title": "Length, Height, Mass and Capacity",
        "seo_title": "Year 1 Measurement Worksheets: Longer, Taller, Heavier, Full and Half Full (Free, with Answers)",
        "short_title": "Length, height, mass and capacity",
        "domain": "Measurement",
        "standard_code": "Year 1: Measurement",
        "standard_url": "https://www.gov.uk/government/publications/national-curriculum-in-england-mathematics-programmes-of-study",
        "standard_text": "Compare, describe and solve practical problems for: lengths and heights [for example, long/short, "
                         "longer/shorter, tall/short, double/half]; mass/weight [for example, heavy/light, heavier than, lighter than]; "
                         "capacity and volume [for example, full/empty, more than, less than, half, half full, quarter]; "
                         "measure and begin to record lengths and heights, mass/weight, capacity and volume.",
        "meta_desc": "Free Year 1 maths worksheets on measuring: longer, shorter and taller, measuring with cubes and paper clips, "
                     "heavier and lighter on a balance, and full, empty, half full and quarter full. 100 picture questions "
                     "with an answer key, matched to the National Curriculum.",
        "key_big": "Line up the ends to compare. The heavier side goes down. Look at how high the water comes.",
        "key_sub": "To measure, lay cubes end to end with no gaps and count them. A bigger thing is not always heavier. "
                   "Half full means the water reaches the middle.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }


if __name__ == "__main__":
    out = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, out["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(out, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
