# -*- coding: utf-8 -*-
"""
Singapore Primary 1 Maths: Length (MOE 2021 Primary Mathematics Syllabus, Measurement:
"Measuring length in centimetres; use of cm; comparing and ordering lengths;
measuring and drawing a line segment to the nearest cm")
  python3 tools/gen_sg_maths_p1_length.py
HTML attributes use single quotes (no backslashes in the JSON).
Primary 1: numbers to 100, very short sentences for 6-7 year olds, a picture in almost every question.
Sets: longer and shorter (lined up, standing up, not lined up), reading a centimetre ruler from 0
(and to the nearest cm), objects that do not start at 0, comparing and ordering lengths in cm,
and word problems within 100.
Every object is drawn exactly from its start mark to its end mark, and every answer is checked in code.
Wrong answers come from real mistakes: starting at 1 / counting the marks instead of the spaces,
reading the end mark when the object does not start at 0, reading the mark before or after the end,
not lining up the ends, comparing the ones digits instead of the tens, adding instead of subtracting,
and forgetting to rename.
"""
import json, math, os, random, re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "sg", "maths", "primary-1")
UPDATED = "2026-11-03"
GREEN = "#006633"
RED = "#c0392b"
INK = "#2b2b2b"
GREY = "#8a8a8a"
RULER = "#f6e7a8"
FONT = "Arial, Helvetica, sans-serif"
GIRLS = ["Siti", "Nurul", "Farah", "Mei Ling", "Hui Min", "Xin Yi", "Priya", "Devi", "Kavya", "Chloe", "Sarah"]
BOYS = ["Ali", "Ahmad", "Hafiz", "Wei Ming", "Jun Jie", "Zhi Hao", "Raju", "Kumar", "Arjun", "Ethan", "Ryan"]

PX = 24          # one grid step in the comparison pictures; one centimetre on a ruler picture
BAND = 24
PADL = 16


def cm(n):
    return "%d cm" % n


# ------------------------------------------------------------ helpers
def mcq(q, correct, cands, e, lock=False):
    """4 choices: correct + the first 3 unique distractors. lock=True keeps the given order (picture labels A-D)."""
    correct = str(correct)
    if lock:
        assert len(cands) == 4 and len(set(cands)) == 4 and correct in cands
        return {"q": q, "c": list(cands), "a": cands.index(correct), "e": e, "lock": True}
    seen = {correct}
    pick = []
    for c in cands:
        if c is None:
            continue
        c = str(c)
        if c in seen or not c or c.startswith("-") or re.match(r"^0\b", c):
            continue
        seen.add(c)
        pick.append(c)
        if len(pick) == 3:
            break
    assert len(pick) == 3, (q, correct, cands)
    return {"q": q, "c": [correct] + pick, "a": 0, "e": e}


def mcq_cm(q, L, cands, e):
    return mcq(q, cm(L), [cm(c) if isinstance(c, int) else c for c in cands
                          if c is not None and (not isinstance(c, int) or 0 < c <= 100)], e)


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


def the(k):
    return "the " + k


def fig(svg):
    return "<div class='qfig'>" + svg + "</div>"


def svg_wrap(w, h, body, label, lg=True):
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


def digit_slip(a, b):
    """Common mistake: subtract the smaller digit from the bigger one in each place (50 − 18 -> 48)."""
    if a < 10 or b < 10:
        return None
    r = abs(a // 10 - b // 10) * 10 + abs(a % 10 - b % 10)
    return r if r != a - b else None


# ------------------------------------------------------------ objects (drawn from x0 to x1 in the band yt..yb)
def draw_object(kind, x0, x1, yt, yb):
    ym = (yt + yb) / 2.0
    L = x1 - x0
    s = []
    if kind == "pencil":
        assert L >= 60, L
        s.append("<rect x='%.1f' y='%.1f' width='9' height='%.1f' fill='#f2a7b5' stroke='%s' stroke-width='1.2'/>" % (x0, yt + 2, yb - yt - 4, INK))
        s.append("<rect x='%.1f' y='%.1f' width='6' height='%.1f' fill='#b8b8b8' stroke='%s' stroke-width='1.2'/>" % (x0 + 9, yt + 1, yb - yt - 2, INK))
        s.append("<rect x='%.1f' y='%.1f' width='%.1f' height='%.1f' fill='#f4c430' stroke='%s' stroke-width='1.2'/>" % (x0 + 15, yt + 1, L - 33, yb - yt - 2, INK))
        s.append("<polygon points='%.1f,%.1f %.1f,%.1f %.1f,%.1f' fill='#e8c79a' stroke='%s' stroke-width='1.2' stroke-linejoin='round'/>"
                 % (x1 - 18, yt + 1, x1 - 18, yb - 1, x1, ym, INK))
        s.append("<polygon points='%.1f,%.1f %.1f,%.1f %.1f,%.1f' fill='%s'/>" % (x1 - 6, ym - 3.6, x1 - 6, ym + 3.6, x1, ym, INK))
    elif kind == "crayon":
        assert L >= 40, L
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
    elif kind == "ice cream stick":
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
        assert L >= 60, L
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


# ------------------------------------------------------------ comparison pictures (no ruler)
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
    """objs: list of (kind, length). The objects stand up on one table top."""
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
    return svg_wrap(W, base + 8, "".join(s), "objects standing on a table: " + desc, lg=False)


# ------------------------------------------------------------ centimetre ruler
def fmt(v):
    return ("%d" % v) if v == int(v) else ("%.1f" % v)


def ruler_body(y, rlen):
    """Ruler 0..rlen cm with whole-centimetre marks. Top edge at y (height 42)."""
    X = lambda k: PADL + PX * k
    right = X(rlen) + 16 + 20 + 8
    s = ["<rect x='%.1f' y='%.1f' width='%.1f' height='42' rx='3' fill='%s' stroke='%s' stroke-width='1.5'/>"
         % (PADL - 10, y, right - (PADL - 10), RULER, INK)]
    for k in range(rlen + 1):
        s.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='2'/>" % (X(k), y, X(k), y + 18, INK))
        s.append("<text x='%.1f' y='%.1f' font-size='15' font-weight='700' fill='%s' text-anchor='middle'>%d</text>" % (X(k), y + 36, INK, k))
    s.append("<text x='%.1f' y='%.1f' font-size='14' fill='%s'>cm</text>" % (X(rlen) + 16, y + 36, INK))
    return "".join(s), right + 6


def ruler_svg(objs, rlen=None):
    """objs: list of (kind, start, end). Each object gets its own band above the ruler. Ends may be decimals."""
    X = lambda k: PADL + PX * k
    band, gap = 24, 8
    top = 6
    if rlen is None:
        rlen = min(15, max(10, int(math.ceil(max(b for _, _, b in objs))) + 2))
    rtop = top + len(objs) * (band + gap)
    s = []
    for i, (kind, a, b) in enumerate(objs):
        assert 0 <= a < b <= rlen, (kind, a, b)
        yt = top + i * (band + gap)
        s.append(guide(X(a), yt - 3, rtop))
        s.append(guide(X(b), yt - 3, rtop))
        s.append(draw_object(kind, X(a), X(b), yt, yt + band))
    body, W = ruler_body(rtop, rlen)
    desc = " and ".join("%s from %s to %s" % (k, fmt(a), fmt(b)) for k, a, b in objs)
    return svg_wrap(int(W), int(rtop + 48), "".join(s) + body, "%s above a ruler in centimetres" % desc)


def empty_ruler_svg(start, rlen=10):
    """A ruler with a red dot where a line will start."""
    X = lambda k: PADL + PX * k
    body, W = ruler_body(14, rlen)
    dot = "<circle cx='%.1f' cy='8' r='5' fill='%s'/>" % (X(start), RED)
    return svg_wrap(int(W), 14 + 48, dot + guide(X(start), 8, 14) + body, "a ruler with a dot at %d" % start)


# ------------------------------------------------------------ strips drawn to scale with their lengths
COLS = ["#e05a6a", "#3d7cc9", "#f4c430", "#8cc63f", "#b07cc6"]


def strips_svg(rows, what="strips"):
    """rows: list of (label, [(cm, text, colour), ...]). Drawn to scale from one start line.
    One segment: the text goes after the bar. Several segments: each text sits inside its segment."""
    maxT = max(sum(c for c, _, _ in segs) for _, segs in rows)
    sc = min(10.0, 300.0 / maxT)
    labw = max(len(l) for l, _ in rows) * 9 + 14
    x0 = labw
    bh, gap, top = 24, 12, 6
    s = []
    right = 0
    for i, (lab, segs) in enumerate(rows):
        yt = top + i * (bh + gap)
        s.append(text(x0 - 8, yt + 17, lab, 15, "end"))
        x = x0
        for c, t, col in segs:
            w = c * sc
            s.append("<rect x='%.1f' y='%.1f' width='%.1f' height='%d' fill='%s' stroke='%s' stroke-width='1.2'/>"
                     % (x, yt, w, bh, col, INK))
            if len(segs) > 1:
                assert w >= 9 * len(t) + 8, (t, w)
                s.append(text(x + w / 2, yt + 17, t, 14, "middle", True, INK))
            x += w
        if len(segs) == 1:
            s.append(text(x + 6, yt + 17, segs[0][1], 15, "start"))
            x += 6 + 9 * len(segs[0][1])
        right = max(right, x)
    s.insert(0, "<line x1='%.1f' y1='2' x2='%.1f' y2='%d' stroke='%s' stroke-width='1.5'/>"
             % (x0, x0, top + len(rows) * (bh + gap) - gap + 4, GREY))
    H = top + len(rows) * (bh + gap) - gap + 8
    desc = ", ".join(("%s %s" % (l, " + ".join(t for _, t, _ in segs))).strip() for l, segs in rows)
    return svg_wrap(int(right + 12), H, "".join(s), "%s drawn to scale: %s" % (what, desc))


# ============================================================ set 1: longer and shorter
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
            e = ("The ends are lined up. Look at the other end. The %s goes further. "
                 "The <b>%s is %s</b>." % (big, win, ask))
        else:
            e = ("Both stand on the same table. Look at the tops. The %s reaches higher. "
                 "The <b>%s is %s</b>." % (big, win, ask))
        return mcq(fig(picture) + "Which is %s?" % ask, the(win), [the(lose)] + OTHER, e)

    for objs, ask in [((("pencil", 9), ("crayon", 5)), "longer"), ((("ribbon", 6), ("straw", 10)), "longer"),
                      ((("eraser", 3), ("pencil", 8)), "shorter")]:
        its.append(two(objs, ask, compare_svg([(k, 0, L) for k, L in objs])))
    its.append(two((("crayon", 6), ("key", 6)), "longer", compare_svg([("crayon", 0, 6), ("key", 0, 6)])))
    for objs, ask in [((("strip of paper", 11), ("crayon", 6)), "shorter"), ((("key", 4), ("ribbon", 7)), "longer"),
                      ((("ice cream stick", 8), ("leaf", 4)), "shorter"), ((("worm", 5), ("caterpillar", 8)), "shorter")]:
        its.append(two(objs, ask, compare_svg([(k, 0, L) for k, L in objs])))

    for objs, ask in [((("pencil", 8), ("crayon", 5)), "taller"), ((("marker", 6), ("straw", 9)), "taller"),
                      ((("ice cream stick", 7), ("crayon", 4)), "shorter")]:
        its.append(two(objs, ask, tall_svg(list(objs)), up=True))

    # three objects: longest / shortest
    for objs, ask in [((("pencil", 9), ("crayon", 5), ("ribbon", 7)), "longest"),
                      ((("straw", 8), ("eraser", 3), ("marker", 6)), "shortest"),
                      ((("leaf", 5), ("ice cream stick", 8), ("worm", 10)), "longest"),
                      ((("ribbon", 9), ("key", 4), ("strip of paper", 6)), "shortest")]:
        ls = [L for _, L in objs]
        k = ls.index(max(ls) if ask == "longest" else min(ls))
        win = objs[k][0]
        rest = [the(o) for i, (o, _) in enumerate(objs) if i != k]
        q = fig(compare_svg([(o, 0, L) for o, L in objs])) + "Which is the %s?" % ask
        e = ("The ends are lined up. Look at the other ends. The %s %s. The <b>%s is the %s</b>."
             % (win, "goes the furthest" if ask == "longest" else "stops first", win, ask))
        its.append(mcq(q, the(win), rest + ["They are the same."], e))

    # not lined up
    for (a, la), (b, sb, lb) in [(("pencil", 7), ("crayon", 4, 5)), (("ribbon", 8), ("straw", 5, 6)),
                                 (("marker", 7), ("ice cream stick", 5, 4))]:
        assert la > lb and sb + lb > la
        q = fig(compare_svg([(a, 0, la), (b, sb, lb)], line=False)) + "The ends are not lined up. Which is longer?"
        e = ("The %s ends further along, but it starts later. Slide it back so the ends line up. "
             "Then the %s goes past it. The <b>%s is longer</b>." % (b, a, a))
        its.append(mcq(q, the(a), [the(b)] + OTHER, e))

    its.append(mcq("You want to find the longer pencil. What do you do first?", "Line up the ends.",
                   ["Look at the colours.", "Count the pencils.", "Look at the tips only."],
                   "Put the pencils side by side. <b>Line up one end</b>. Then look at the other end. "
                   "The one that goes further is longer."))
    a, m = P.next(), P.next()
    its.append(mcq("%s’s ribbon is shorter than %s’s ribbon. Which is true?" % (a[0], m[0]),
                   "%s’s is longer." % m[0],
                   ["%s’s is longer." % a[0], "They are the same.", "%s’s is shorter." % m[0]],
                   "If %s’s ribbon is shorter, then %s’s ribbon is longer. <b>%s’s is longer</b>." % (a[0], m[0], m[0])))
    order = [0, 1, 2, 3, 4, 5, 11, 6, 7, 8, 12, 9, 10, 18, 13, 14, 19, 15, 16, 17]
    assert sorted(order) == list(range(20))
    its = [its[i] for i in order]
    assert len(its) == 20, len(its)
    return {"title": "Longer and shorter", "items": its}


# ============================================================ set 2: measure with a ruler from 0
S2 = [("eraser", 2), ("paper clip", 3), ("key", 4), ("crayon", 5), ("leaf", 6), ("caterpillar", 7), ("worm", 8),
      ("pencil", 9), ("straw", 10), ("marker", 11), ("ice cream stick", 12), ("ribbon", 13)]


def zero_e(obj, L):
    e = "The %s starts at 0 and ends at %d. " % (obj, L)
    if L <= 8:
        e += "Count the spaces: %s. " % count_list(L)
    e += "It is <b>%d cm</b> long. There are %d marks but only %d spaces. Count the spaces, not the marks." % (L, L + 1, L)
    return e


def set_from_zero(P):
    its = []
    its.append(mcq("You measure with a ruler. Where do you put one end of the object?", "at the 0 mark",
                   ["at the 1 mark", "at the edge of the ruler", "anywhere"],
                   "Put the end at <b>0</b>. Some rulers have a little space before the 0, so do not use the edge. "
                   "If you start at 1, the number at the end is 1 too big."))
    asks = ["How long is the %s?", "How many centimetres long is the %s?", "Measure the %s. How long is it?"]
    for i, (obj, L) in enumerate(S2):
        q = fig(ruler_svg([(obj, 0, L)])) + asks[i % 3] % obj
        its.append(mcq_cm(q, L, [L + 1, L - 1, L + 2, "%d m" % L], zero_e(obj, L)))
        if i == 5:
            its.append(mcq("What do you count to find a length on a ruler?", "the spaces",
                           ["the marks", "all the numbers", "the last number on the ruler"],
                           "Each space from one mark to the next is 1 cm. Count the <b>spaces</b>, not the marks. "
                           "A 3 cm eraser covers 3 spaces but touches 4 marks."))
    # to the nearest cm
    for obj, b in [("pencil", 6.8), ("strip of paper", 9.2)]:
        n = int(round(b))
        lo, hi = int(math.floor(b)), int(math.ceil(b))
        far = hi if n == lo else lo
        q = fig(ruler_svg([(obj, 0, b)])) + "The end is not on a mark. About how long is the %s?" % obj
        e = ("The end is between %d and %d. It is closer to <b>%d</b>. So the %s is <b>about %d cm</b> long."
             % (lo, hi, n, obj, n))
        its.append(mcq(q, "about %d cm" % n, ["about %d cm" % far, "about %d cm" % (n + 1 if far < n else n - 1),
                                              "about %d cm" % (n + 2 if far < n else n - 2)], e))
    nm, he, his = P.next()
    q = fig(ruler_svg([("line", 0, 7)])) + "%s drew this red line. How long is it?" % nm
    its.append(mcq_cm(q, 7, [8, 6, 14],
                      "The line starts at 0 and ends at 7. It covers 7 spaces, so it is <b>7 cm</b> long. "
                      "There are 8 marks, but count the spaces."))
    nm, he, his = P.next()
    q = fig(ruler_svg([("crayon", 0, 6)])) + "%s says the crayon is 7 cm long. What did %s do wrong?" % (nm, he)
    its.append(mcq(q, "%s counted the marks." % cap(he),
                   ["%s started at 0." % cap(he), "%s counted the spaces." % cap(he), "%s measured in m." % cap(he)],
                   "The crayon starts at 0 and ends at 6, so it is 6 cm long. %s counted 7 marks. "
                   "<b>Count the spaces, not the marks.</b>" % nm))
    nm, he, his = P.next()
    q = fig(empty_ruler_svg(0)) + "%s wants to draw a line 6 cm long. %s starts at 0. Where should %s stop?" % (nm, cap(he), he)
    its.append(mcq(q, "at 6", ["at 7", "at 5", "at 12"],
                   "Start at 0 and draw to <b>6</b>. That covers 6 spaces, so the line is 6 cm long. "
                   "If you stop at 7, the line is 7 cm long."))
    nm, he, his = P.next()
    q = fig(ruler_svg([("line", 0, 5)])) + "%s wants a line 8 cm long. %s drew this much. How many more centimetres must %s draw?" % (nm, cap(he), he)
    its.append(mcq_cm(q, 3, [8, 5, 13, 4],
                      "The line ends at 5. %s needs to get to 8. Count on from 5: 6, 7, 8. That is 3 spaces. "
                      "8 − 5 = 3, so %s must draw <b>3 cm</b> more." % (nm, he)))
    assert len(its) == 20, len(its)
    return {"title": "Measure with a ruler from 0", "items": its}


# ============================================================ set 3: not starting at 0
S3 = [("eraser", 1, 4), ("crayon", 2, 7), ("key", 3, 6), ("leaf", 1, 8), ("caterpillar", 4, 9), ("paper clip", 5, 8),
      ("marker", 2, 10), ("worm", 6, 13), ("straw", 3, 12), ("pencil", 1, 11), ("ice cream stick", 5, 14), ("ribbon", 4, 15)]


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
    q = fig(ruler_svg([("crayon", 3, 8)])) + "Where does the crayon start?"
    its.append(mcq(q, "at 3", ["at 0", "at 8", "at 5"],
                   "Look at the left end of the crayon. It is at the <b>3</b> mark, not at 0. "
                   "So you cannot just read the number at the other end."))
    for i, (obj, a, b) in enumerate(S3):
        L = b - a
        q = fig(ruler_svg([(obj, a, b)])) + ("How long is the %s?" if i % 2 == 0 else
                                             "The %s does not start at 0. How many centimetres long is it?") % obj
        its.append(mcq_cm(q, L, [b, L + 1, a, L - 1, a + b], not_zero_e(obj, a, b)))

    nm, he, his = P.next()
    q = fig(ruler_svg([("crayon", 1, 9)])) + "%s says the crayon is 9 cm long. What did %s do wrong?" % (nm, he)
    its.append(mcq(q, "%s read the end number." % cap(he),
                   ["%s counted the spaces." % cap(he), "%s started at 0." % cap(he), "%s measured in m." % cap(he)],
                   "The crayon starts at 1, not at 0, so 9 is too big. 9 − 1 = 8. The crayon is 8 cm long."))
    nm, he, his = P.next()
    its.append(mcq_cm("The end of %s’s ruler is broken. It starts at 4. A paper clip goes from 4 to 7. "
                      "How long is it?" % nm, 3, [7, 4, 11],
                      "Count from 4, not from 0: 5, 6, 7 is 3 spaces. 7 − 4 = 3, so the paper clip is <b>3 cm</b> long."))
    nm, he, his = P.next()
    its.append(mcq_cm("A pencil goes from 3 to 12 on a ruler. %s counts the marks and gets 10. "
                      "How long is the pencil?" % nm, 9, [10, 12, 15],
                      "Count spaces, not marks. From 3 to 12 there are 10 marks but only 9 spaces. 12 − 3 = 9, "
                      "so the pencil is <b>9 cm</b> long."))
    q = fig(ruler_svg([("crayon", 0, 5), ("key", 3, 8)])) + "Look at the crayon and the key. Which is true?"
    its.append(mcq(q, "They are the same length.", ["The key is longer.", "The crayon is longer.", "You cannot tell."],
                   "The crayon goes from 0 to 5: 5 cm. The key goes from 3 to 8: 8 − 3 = 5 cm. "
                   "<b>They are the same length.</b> The key ends at a bigger number, but it also starts later."))
    nm, he, his = P.next()
    q = fig(empty_ruler_svg(4, 12)) + "%s starts a line at 4. %s draws it 6 cm long. Where does the line end?" % (nm, cap(he))
    its.append(mcq(q, "at 10", ["at 6", "at 9", "at 11"],
                   "Start at 4 and count 6 spaces: 5, 6, 7, 8, 9, 10. Or add: 4 + 6 = 10. The line ends <b>at 10</b>."))
    nm, he, his = P.next()
    q = fig(empty_ruler_svg(2, 11)) + "%s starts a line at 2. %s wants it to be 7 cm long. Where should %s stop?" % (nm, cap(he), he)
    its.append(mcq(q, "at 9", ["at 7", "at 8", "at 5"],
                   "Start at 2 and count 7 spaces: 3, 4, 5, 6, 7, 8, 9. Or add: 2 + 7 = 9. Stop <b>at 9</b>. "
                   "If you stop at 7, the line is only 5 cm long."))
    # 0 = start q, 1..12 pictures, 13 wrong, 14 broken, 15 marks, 16 same, 17 line end, 18 line stop -> 19 items
    nm, he, his = P.next()
    its.append(mcq_cm("%s measures a key. One end is at 5. The other end is at 9. How long is the key?" % nm,
                      4, [9, 5, 14, 3],
                      "The key starts at 5, not at 0. Count the spaces from 5 to 9: 6, 7, 8, 9. That is 4. "
                      "Or subtract: 9 − 5 = 4. The key is <b>4 cm</b> long."))
    order = [0, 1, 2, 3, 4, 13, 5, 6, 7, 14, 8, 9, 19, 10, 15, 11, 12, 16, 17, 18]
    assert sorted(order) == list(range(20))
    its = [its[i] for i in order]
    assert len(its) == 20, len(its)
    return {"title": "When the object does not start at 0", "items": its}


# ============================================================ set 4: compare and order in cm
def set_order(P):
    its = []
    for A, a, B, b, ask in [("pencil", 9, "crayon", 6, "longer"), ("straw", 7, "marker", 11, "shorter")]:
        q = fig(ruler_svg([(A, 0, a), (B, 0, b)])) + "Which is %s?" % ask
        win = A if (a > b) == (ask == "longer") else B
        lose = B if win == A else A
        e = ("The %s is %d cm. The %s is %d cm. %d is %s than %d. The <b>%s is %s</b>."
             % (A, a, B, b, max(a, b) if ask == "longer" else min(a, b), "more" if ask == "longer" else "less",
                min(a, b) if ask == "longer" else max(a, b), win, ask))
        its.append(mcq(q, the(win), [the(lose), "They are the same.", "You cannot tell."], e))
    for A, a, B, b in [("pencil", 12, "crayon", 7), ("straw", 10, "eraser", 3), ("ribbon", 13, "key", 6)]:
        d = a - b
        q = fig(ruler_svg([(A, 0, a), (B, 0, b)])) + "How much longer is the %s than the %s?" % (A, B)
        e = ("Both start at 0. The %s ends at %d. The %s ends at %d. %d − %d = %d. The %s is <b>%d cm</b> longer."
             % (A, a, B, b, a, b, d, A, d))
        its.append(mcq_cm(q, d, [a, a + b, d + 1, d - 1], e))
    q = fig(ruler_svg([("pencil", 0, 9), ("crayon", 0, 4)])) + "How much shorter is the crayon than the pencil?"
    its.append(mcq_cm(q, 5, [4, 13, 9, 6],
                      "The pencil is 9 cm. The crayon is 4 cm. 9 − 4 = 5. The crayon is <b>5 cm</b> shorter."))
    # not lined up on the ruler
    q = fig(ruler_svg([("straw", 0, 7), ("pencil", 5, 11)])) + "Which is longer?"
    its.append(mcq(q, "the straw", ["the pencil", "They are the same.", "You cannot tell."],
                   "The straw goes from 0 to 7: 7 cm. The pencil goes from 5 to 11: 11 − 5 = 6 cm. "
                   "<b>The straw</b> is longer, even though the pencil ends at a bigger number."))
    q = fig(ruler_svg([("marker", 0, 5), ("ice cream stick", 3, 12)])) + "Which is longer?"
    its.append(mcq(q, "the ice cream stick", ["the marker", "They are the same.", "You cannot tell."],
                   "The marker goes from 0 to 5: 5 cm. The ice cream stick goes from 3 to 12: 12 − 3 = 9 cm. "
                   "9 is more than 5, so <b>the ice cream stick</b> is longer."))
    # three objects on a ruler
    trio = [("pencil", 0, 10), ("crayon", 0, 6), ("key", 0, 4)]
    q = fig(ruler_svg(trio)) + "Order them from shortest to longest."
    its.append(mcq(q, "key, crayon, pencil", ["pencil, crayon, key", "crayon, key, pencil", "key, pencil, crayon"],
                   "The key is 4 cm, the crayon is 6 cm and the pencil is 10 cm. Shortest first: "
                   "<b>key, crayon, pencil</b>."))
    trio = [("straw", 0, 8), ("marker", 0, 11), ("eraser", 0, 3)]
    q = fig(ruler_svg(trio)) + "Which is the longest?"
    its.append(mcq(q, "the marker", ["the straw", "the eraser", "They are the same."],
                   "The straw is 8 cm, the marker is 11 cm and the eraser is 3 cm. 11 is the biggest number, "
                   "so <b>the marker</b> is the longest."))

    # ribbons with lengths in cm (drawn to scale), labels A-D
    def ribbons(lens, what="ribbons"):
        return strips_svg([(L, [(n, cm(n), COLS[i])]) for i, (L, n) in enumerate(zip("ABCD", lens))], what)

    for lens, ask in [((24, 42, 35, 18), "longest"), ((31, 13, 26, 30), "shortest")]:
        k = lens.index(max(lens) if ask == "longest" else min(lens))
        q = fig(ribbons(lens)) + "Which ribbon is the %s?" % ask
        tens = ", ".join("%d ten%s" % (n // 10, "" if n // 10 == 1 else "s") for n in lens)
        e = ("Compare the tens first: %s. Ribbon %s is <b>%d cm</b>, so <b>Ribbon %s</b> is the %s."
             % (tens, "ABCD"[k], lens[k], "ABCD"[k], ask))
        its.append(mcq(q, "Ribbon " + "ABCD"[k], ["Ribbon " + x for x in "ABCD"], e, lock=True))
    lens = (21, 32, 12, 25)
    q = fig(ribbons(lens)) + "Which ribbon is shorter than 20 cm?"
    its.append(mcq(q, "Ribbon C", ["Ribbon " + x for x in "ABCD"],
                   "20 has 2 tens. Ribbon C is 12 cm. 12 has only 1 ten, so <b>Ribbon C</b> is shorter than 20 cm. "
                   "21 cm is a little longer than 20 cm.", lock=True))
    lens = (52, 25, 38)
    q = fig(strips_svg([(L, [(n, cm(n), COLS[i])]) for i, (L, n) in enumerate(zip("ABC", lens))])) + \
        "Order the strips from longest to shortest."
    its.append(mcq(q, "A, C, B", ["B, C, A", "A, B, C", "C, A, B"],
                   "52 cm is the longest. 38 cm is next. 25 cm is the shortest. Longest first: <b>A, C, B</b>. "
                   "Do not order by the ones: 25 has 2 tens, so it is the shortest."))
    lens = (47, 74, 60)
    q = fig(strips_svg([(L, [(n, cm(n), COLS[i + 1])]) for i, (L, n) in enumerate(zip("ABC", lens))])) + \
        "Order the strips from shortest to longest."
    its.append(mcq(q, "A, C, B", ["B, C, A", "C, A, B", "A, B, C"],
                   "47 cm has 4 tens, 60 cm has 6 tens and 74 cm has 7 tens. Shortest first: <b>A, C, B</b>."))
    a, m = P.next(), P.next()
    q = fig(strips_svg([(a[0], [(46, "46 cm", COLS[0])]), (m[0], [(64, "64 cm", COLS[1])])], "strings")) + \
        "Whose string is longer?"
    its.append(mcq(q, "%s’s string" % m[0], ["%s’s string" % a[0], "They are the same.", "You cannot tell."],
                   "46 has 4 tens. 64 has 6 tens. 6 tens is more, so <b>%s’s string</b> is longer. "
                   "Same digits, but the tens are different." % m[0]))
    # text only (numbers)
    its.append(mcq("Which length is the longest?", "83 cm", ["38 cm", "58 cm", "80 cm"],
                   "Compare the tens first. 83 and 80 both have 8 tens. Then compare the ones: 3 is more than 0. "
                   "So <b>83 cm</b> is the longest."))
    its.append(mcq("Which length is shorter than 25 cm?", "19 cm", ["52 cm", "27 cm", "25 cm"],
                   "19 has 1 ten. 25 has 2 tens. So <b>19 cm</b> is shorter. 25 cm is not shorter than 25 cm. "
                   "It is the same."))
    its.append(mcq("47 cm is ____ than 74 cm.", "shorter", ["longer", "taller", "the same"],
                   "47 has 4 tens. 74 has 7 tens. 47 is less than 74, so 47 cm is <b>shorter</b>."))
    its.append(mcq("Order from shortest to longest: 61 cm, 16 cm, 60 cm", "16 cm, 60 cm, 61 cm",
                   ["61 cm, 60 cm, 16 cm", "60 cm, 61 cm, 16 cm", "16 cm, 61 cm, 60 cm"],
                   "16 has only 1 ten, so it is the shortest. 60 and 61 both have 6 tens. 0 ones is less than 1 one. "
                   "So the order is <b>16 cm, 60 cm, 61 cm</b>."))
    assert len(its) == 20, len(its)
    return {"title": "Compare and order lengths in cm", "items": its}


# ============================================================ set 5: word problems
def diff_e(a, b, d):
    e = "Find the difference. Subtract: %d − %d = <b>%d cm</b>. " % (a, b, d)
    if 2 <= d <= 6:
        e += "Or count on from %d to %d: %s. " % (b, a, count_list(d, b + 1))
    elif a >= 20:
        e += "Check: %d + %d = %d. " % (b, d, a)
    if a + b <= 100:
        e += "Do not add. %d + %d = %d is the total, not the difference." % (a, b, a + b)
    return e


def set_problems(P):
    its = []

    def strip2(n1, l1, n2, l2, what="ribbons"):
        return fig(strips_svg([(n1, [(l1, cm(l1), COLS[0])]), (n2, [(l2, cm(l2), COLS[1])])], what))

    def sub_c(a, b):
        d = a - b
        return [digit_slip(a, b), a + b, d + 1, d - 1, d + 10, a]

    def add_c(a, b):
        t = a + b
        noreg = t - 10 if (a % 10 + b % 10) >= 10 else None
        return [noreg, abs(a - b) if a != b else None, t + 1, t - 1, t + 10]

    # 1 how much longer (small numbers)
    a, m = P.next(), P.next()
    q = strip2("%s" % a[0], 14, m[0], 9) + "%s’s ribbon is 14 cm long. %s’s ribbon is 9 cm long. How much longer is %s’s ribbon?" % (a[0], m[0], a[0])
    its.append(mcq_cm(q, 5, sub_c(14, 9), diff_e(14, 9, 5)))
    # 2 sharpened pencil
    nm, he, his = P.next()
    q = fig(strips_svg([("before", [(17, "17 cm", "#f4c430")]), ("now", [(12, "12 cm", "#f4c430")])], "pencil")) + \
        "%s’s pencil was 17 cm long. %s sharpened it. Now it is 12 cm. How much shorter is it?" % (nm, cap(he))
    its.append(mcq_cm(q, 5, sub_c(17, 12), diff_e(17, 12, 5)))
    # 3 join two strips
    nm, he, his = P.next()
    q = fig(strips_svg([("", [(24, "24 cm", COLS[2]), (15, "15 cm", COLS[3])])], "two strips joined")) + \
        "%s joins two paper strips end to end. How long is the long strip now?" % nm
    its.append(mcq_cm(q, 39, add_c(24, 15),
                      "Joining end to end makes it longer, so add: 24 + 15 = <b>39 cm</b>. 2 tens + 1 ten = 3 tens. 4 + 5 = 9 ones."))
    # 4 plant grows
    nm, he, his = P.next()
    q = fig(strips_svg([("Monday", [(8, "8 cm", COLS[3])]), ("Friday", [(8, "8 cm", COLS[3]), (5, "5 cm", "#c9e6a8")])], "plant height")) + \
        "%s’s bean plant was 8 cm tall. It grew 5 cm more. How tall is it now?" % nm
    its.append(mcq_cm(q, 13, [3, 12, 14, 85, 58],
                      "It grew, so add: 8 + 5 = <b>13 cm</b>. Count on from 8: 9, 10, 11, 12, 13."))
    # 5 two ice cream sticks
    nm, he, his = P.next()
    q = fig(strips_svg([("", [(11, "11 cm", "#e6c88f"), (11, "11 cm", "#e6c88f")])], "two ice cream sticks")) + \
        "%s puts two ice cream sticks end to end. Each is 11 cm long. How long are they together?" % nm
    its.append(mcq_cm(q, 22, [11, 21, 23, 12, 33],
                      "Add the two lengths: 11 + 11 = <b>22 cm</b>."))
    # 6 bubble tea straw
    q = strip2("bubble tea", 21, "small", 15, "straws") + \
        "A bubble tea straw is 21 cm long. A small straw is 15 cm long. How much longer is the bubble tea straw?"
    its.append(mcq_cm(q, 6, sub_c(21, 15), diff_e(21, 15, 6)))
    # 7 chopsticks and spoon
    nm, he, his = P.next()
    q = strip2("chopstick", 23, "spoon", 14, "chopstick and spoon") + \
        "At the hawker centre, %s’s chopstick is 23 cm long. %s spoon is 14 cm long. How much shorter is the spoon?" % (nm, cap(his))
    its.append(mcq_cm(q, 9, sub_c(23, 14), diff_e(23, 14, 9)))
    # 8 cut ribbon (renaming)
    nm, he, his = P.next()
    q = fig(strips_svg([("", [(18, "18 cm", COLS[1]), (32, "?", COLS[0])])], "a ribbon cut into two parts")) + \
        ("%s has a ribbon 50 cm long. %s cuts off 18 cm for a Children’s Day card. How much ribbon is left?"
         % (nm, cap(he)))
    its.append(mcq_cm(q, 32, sub_c(50, 18),
                      "Take away the part cut off: 50 − 18 = <b>32 cm</b>. Rename 5 tens as 4 tens 10 ones. "
                      "10 − 8 = 2, 4 − 1 = 3. Check: 18 + 32 = 50."))
    # 9 more ribbon needed
    nm, he, his = P.next()
    q = fig(strips_svg([("has", [(45, "45 cm", COLS[0])]), ("needs", [(60, "60 cm", COLS[4])])], "ribbons")) + \
        "%s needs 60 cm of ribbon. %s has 45 cm. How many more centimetres does %s need?" % (nm, cap(he), he)
    its.append(mcq_cm(q, 15, sub_c(60, 45), diff_e(60, 45, 15)))
    # 10 longer than (add)
    a, m = P.next(), P.next()
    q = strip2(a[0], 28, m[0], 37) + \
        "%s’s hair ribbon is 28 cm long. %s’s hair ribbon is 9 cm longer. How long is %s’s ribbon?" % (a[0], m[0], m[0])
    q = q.replace("37 cm</text>", "?</text>", 1)
    its.append(mcq_cm(q, 37, add_c(28, 9),
                      "“Longer” means more, so add: 28 + 9 = <b>37 cm</b>. 8 + 9 = 17 ones. Rename 10 ones as 1 ten."))
    # 11 shorter than (subtract)
    a, m = P.next(), P.next()
    q = strip2(a[0], 52, m[0], 37, "strings") + \
        "%s’s string is 52 cm long. %s’s string is 15 cm shorter. How long is %s’s string?" % (a[0], m[0], m[0])
    q = q.replace("37 cm</text>", "?</text>", 1)
    its.append(mcq_cm(q, 37, [67, 43, 38, 36, 47],
                      "“Shorter” means less, so subtract: 52 − 15 = <b>37 cm</b>. Rename 5 tens 2 ones as 4 tens 12 ones. "
                      "12 − 5 = 7, 4 − 1 = 3."))
    # 12 mistake on the ruler
    nm, he, his = P.next()
    q = fig(ruler_svg([("pencil", 2, 11)])) + "%s says the pencil is 11 cm long. How long is it really?" % nm
    its.append(mcq_cm(q, 9, [11, 10, 13, 2],
                      "The pencil starts at 2, not at 0. %s read the end number. 11 − 2 = <b>9 cm</b>." % nm))
    # 13 extend a line
    nm, he, his = P.next()
    q = fig(ruler_svg([("line", 0, 5)])) + "%s drew this line. Then %s made it 4 cm longer. How long is the line now?" % (nm, he)
    its.append(mcq_cm(q, 9, [4, 5, 1, 10, 8],
                      "The line is 5 cm. Add 4 cm more: 5 + 4 = <b>9 cm</b>. It now ends at 9."))
    # 14 tallest plant (order)
    q = fig(strips_svg([("Ali", [(34, "34 cm", COLS[3])]), ("Siti", [(43, "43 cm", COLS[3])]),
                        ("Raju", [(29, "29 cm", COLS[3])])], "plant heights")) + \
        "Ali, Siti and Raju each grow a plant. Whose plant is the tallest?"
    its.append(mcq(q, "Siti’s plant", ["Ali’s plant", "Raju’s plant", "They are the same."],
                   "Compare the tens: 34 has 3 tens, 43 has 4 tens, 29 has 2 tens. 43 cm is the most. "
                   "<b>Siti’s plant</b> is the tallest."))
    # 15 three ribbons of 10 cm
    nm, he, his = P.next()
    q = fig(strips_svg([("", [(10, "10 cm", COLS[0]), (10, "10 cm", COLS[1]), (10, "10 cm", COLS[2])])], "three ribbons joined")) + \
        "%s joins 3 ribbons end to end. Each ribbon is 10 cm long. How long is the long ribbon?" % nm
    its.append(mcq_cm(q, 30, [20, 13, 10, 40],
                      "Count in tens: 10, 20, 30. Or add: 10 + 10 + 10 = <b>30 cm</b>."))
    # 16 pencil in pencil case
    nm, he, his = P.next()
    q = strip2("pencil case", 20, "pencil", 17, "pencil case and pencil") + \
        "%s’s pencil case is 20 cm long. %s pencil is 17 cm long. How much longer is the pencil case?" % (nm, cap(his))
    its.append(mcq_cm(q, 3, sub_c(20, 17), diff_e(20, 17, 3)))
    # 17 red packet strips (CNY)
    q = strip2("red", 45, "gold", 30, "paper strips") + \
        "For Chinese New Year, Mrs Lim cuts a red strip 45 cm long and a gold strip 30 cm long. How much longer is the red strip?"
    its.append(mcq_cm(q, 15, sub_c(45, 30), diff_e(45, 30, 15)))
    # 18 paper chain (renaming)
    nm, he, his = P.next()
    q = fig(strips_svg([("", [(45, "45 cm", COLS[4]), (38, "38 cm", COLS[2])])], "two paper chains joined")) + \
        "%s makes a paper chain for National Day. One part is 45 cm. The other part is 38 cm. %s joins them. How long is the chain?" % (nm, cap(he))
    its.append(mcq_cm(q, 83, add_c(45, 38),
                      "Joining makes it longer, so add: 45 + 38 = <b>83 cm</b>. 5 + 8 = 13 ones. "
                      "Rename 10 ones as 1 ten. 4 + 3 + 1 = 8 tens."))
    # 19 caterpillar and worm
    a, m = P.next(), P.next()
    q = fig(ruler_svg([("worm", 0, 9), ("caterpillar", 0, 4)])) + \
        "At East Coast Park, %s found this worm and caterpillar. How much longer is the worm?" % a[0]
    its.append(mcq_cm(q, 5, [9, 13, 4, 6],
                      "The worm is 9 cm. The caterpillar is 4 cm. 9 − 4 = <b>5 cm</b>."))
    # 20 two steps
    nm, he, his = P.next()
    q = fig(strips_svg([("", [(30, "30 cm", COLS[1]), (12, "12 cm", COLS[0]), (18, "?", "#dddddd")])], "a 60 cm ribbon in three parts")) + \
        ("%s has a ribbon 60 cm long. %s uses 30 cm for a bow. %s uses 12 cm for a card. How much is left?"
         % (nm, cap(he), cap(he)))
    its.append(mcq_cm(q, 18, [42, 30, 28, 102, 22],
                      "First: 60 − 30 = 30. Then: 30 − 12 = <b>18 cm</b>. Check: 30 + 12 + 18 = 60."))
    assert len(its) == 20, len(its)
    order = [0, 1, 3, 4, 12, 18, 15, 2, 14, 5, 6, 11, 13, 16, 8, 7, 9, 10, 17, 19]
    assert sorted(order) == list(range(20))
    its = [its[i] for i in order]
    return {"title": "Length word problems", "items": its}


# ============================================================ lesson
def body_html():
    return (
        "<h2>Longer and shorter</h2>"
        "<p>To compare two things, <b>line up one end</b>. Then look at the other end. "
        "The one that goes further is <b>longer</b>. The other one is <b>shorter</b>.</p>"
        "<figure class='sn-fig'>" + compare_svg([("pencil", 0, 9), ("crayon", 0, 5)]) +
        "<figcaption>The ends are lined up. The pencil is longer. The crayon is shorter.</figcaption></figure>"
        "<h2>Measure in centimetres (cm)</h2>"
        "<p>We measure short lengths in <b>centimetres</b>. We write <b>cm</b>. "
        "Put one end of the object at the <b>0</b> mark. Look where the other end stops. "
        "Each space between two marks is 1 cm. Count the spaces, not the marks.</p>"
        "<figure class='sn-fig'>" + ruler_svg([("pencil", 0, 6)]) +
        "<figcaption>The pencil starts at 0 and ends at 6. It is 6 cm long.</figcaption></figure>"
        "<p>If the end is between two marks, choose the <b>nearest</b> mark.</p>"
        "<figure class='sn-fig'>" + ruler_svg([("strip of paper", 0, 6.8)]) +
        "<figcaption>The end is closer to 7 than to 6. The strip is about 7 cm long.</figcaption></figure>"
        "<h2>When the object does not start at 0</h2>"
        "<p>Count the spaces from where it starts to where it ends. Or subtract: end − start.</p>"
        "<figure class='sn-fig'>" + ruler_svg([("leaf", 3, 10)]) +
        "<figcaption>The leaf starts at 3 and ends at 10. 10 − 3 = 7, so the leaf is 7 cm long, not 10.</figcaption></figure>"
        + ex("Example", "A crayon starts at 2 and ends at 6. How long is it?",
             "Count from 2: 3, 4, 5, 6 is 4 spaces. 6 − 2 = 4.", "4 cm")
        + ex("Draw a line", "Draw a line 5 cm long.",
             "Put a dot at 0. Draw along the ruler to 5. The line covers 5 spaces.", "Stop at the 5 mark")
        + ex("Compare", "A ribbon is 45 cm long. A string is 28 cm long. How much longer is the ribbon?",
             "Subtract: 45 − 28 = 17. Check: 28 + 17 = 45.", "17 cm")
        + "<h2>Common mistakes</h2>"
        + table(["Mistake", "What to do instead"], [
            ["Starting at 1 or at the edge of the ruler", "Line up the end of the object with 0"],
            ["Counting the marks (7 marks for 6 cm)", "Count the spaces between the marks"],
            ["Reading the end number when the object starts at 3", "Subtract the start: 10 − 3 = 7"],
            ["Choosing the mark before the end", "Choose the nearest mark"],
            ["Not lining up the ends when comparing", "Line up one end first"],
            ["Thinking 25 cm is longer than 52 cm", "Compare the tens first"],
        ])
    )


FAQ = [
    {"q": "What is taught in P1 length?",
     "a": "Primary 1 students compare lengths, measure in centimetres with a ruler, and write cm. "
          "They also order lengths and draw a line to the nearest cm."},
    {"q": "How do I teach my child to use a ruler?",
     "a": "Show your child how to put one end of the object at the 0 mark, then read the number where the other end "
          "stops. Ask them to count the spaces between the marks, not the marks."},
    {"q": "What is the most common mistake when measuring length?",
     "a": "The most common mistake is starting at 1, or at the edge of the ruler, instead of at 0. "
          "Children also read the end number when the object does not start at 0, and forget to line up ends."},
    {"q": "Is length in the MOE Primary 1 syllabus?",
     "a": "Yes. Measuring length in centimetres, using cm, comparing and ordering lengths, and measuring and drawing "
          "a line to the nearest cm are part of Measurement in the MOE 2021 Primary 1 Mathematics syllabus."},
]


def gen():
    rnd = random.Random(61808)
    P = People(rnd)
    sets = [set_compare(P), set_from_zero(P), set_not_zero(P), set_order(P), set_problems(P)]
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
    # ruler pictures with one object: the answer is end − start
    n = 0
    for s in sets:
        for it in s["items"]:
            m = re.search(r"aria-label='([a-z ]+) from (\d+) to (\d+) above a ruler", it["q"])
            if m and " and " not in m.group(1) and m.group(1) != "line" and it["q"].rstrip().endswith(("?", "long is it?")) \
                    and it["c"][it["a"]].endswith(" cm") and "say" not in it["q"]:
                assert it["c"][it["a"]] == cm(int(m.group(3)) - int(m.group(2))), it["q"][-80:]
                n += 1
            m = re.search(r"aria-label='([a-z ]+) from 0 to (\d+\.\d) above", it["q"])
            if m:
                assert it["c"][it["a"]] == "about %d cm" % round(float(m.group(2)))
                n += 1
            m = re.search(r"aria-label='([a-z ]+) from 0 to (\d+) and ([a-z ]+) from 0 to (\d+) above", it["q"])
            if m and "How much longer" in it["q"]:
                assert it["c"][it["a"]] == cm(int(m.group(2)) - int(m.group(4)))
                n += 1
    assert n == 12 + 12 + 2 + 3 + 1, n
    u = {
        "country": "sg", "subject": "maths", "grade": "primary-1", "slug": "length", "sort": 8,
        "updated": UPDATED, "pdf_url": "",
        "title": "Primary 1 Length in Centimetres",
        "seo_title": "P1 Length Worksheets: Free Primary 1 Maths on Measuring in cm with Answers (MOE Syllabus)",
        "short_title": "Length",
        "domain": "Measurement and Geometry",
        "standard_code": "Primary 1: Measurement",
        "standard_url": "https://www.moe.gov.sg/primary/curriculum/syllabus",
        "standard_text": "Measuring length in centimetres; use of cm; comparing and ordering lengths; "
                         "measuring and drawing a line segment to the nearest cm",
        "meta_desc": "Free P1 maths practice on length: compare longer and shorter, measure in cm with a ruler, "
                     "order lengths and solve word problems. 100 questions with answers.",
        "key_big": "Put one end at 0 and count the spaces, not the marks.",
        "key_sub": "A crayon from 3 to 10 on the ruler is 10 − 3 = 7 cm long.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }
    assert len(u["meta_desc"]) <= 160, len(u["meta_desc"])
    return u


if __name__ == "__main__":
    out = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, out["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(out, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
