# -*- coding: utf-8 -*-
"""
US Grade 3 Math: Line Plots and Measuring to the Nearest Half and Quarter Inch (3.MD.B.4)
  python tools/gen_us_math_g3_line_plots.py
All lengths are kept as whole numbers of QUARTER inches (q): 10 means 2 1/2 inches.
HTML attributes use single quotes (no backslashes in the JSON).
"""
import json, re, os, random

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "us", "math", "grade-3")
UPDATED = "2026-11-01"
GREEN = "#006633"
RED = "#c0392b"
INK = "#2b2b2b"
GREY = "#8a8a8a"
RULER = "#f6e7a8"
GIRLS = ["Maya", "Ava", "Mia", "Zoe", "Lily", "Emma", "Nora", "Ruby", "Sofia", "Grace"]
BOYS = ["Leo", "Noah", "Eli", "Sam", "Ben", "Omar", "Kai", "Jack", "Luis", "Owen"]
TEACHERS = ["Ms. Lee", "Mr. Diaz", "Mrs. Patel", "Ms. Brown", "Mr. Kim", "Mrs. Green"]


# ------------------------------------------------------------ numbers
def fr(a, b):
    return "<span class='fr'><span class='fn'>%d</span><span class='fd'>%d</span></span>" % (a, b)


def num(q):
    """Mixed number for q quarter inches, as HTML."""
    w, r = divmod(q, 4)
    f = {0: "", 1: fr(1, 4), 2: fr(1, 2), 3: fr(3, 4)}[r]
    if w and f:
        return "%d %s" % (w, f)
    return f or str(w)


def inches(q):
    return "%s %s" % (num(q), "inch" if q <= 4 else "inches")


def ch(q):
    return num(q) + " in"


def nword(n, one, many):
    return "%d %s" % (n, one if n == 1 else many)


# ------------------------------------------------------------ helpers
def mcq(q, correct, cands, e, rnd):
    correct = str(correct)
    seen = {correct}
    pick = []
    for c in cands:
        if c is None:
            continue
        c = str(c)
        if c in seen or not c or c.startswith("-") or c == "0" or c.startswith("0 "):
            continue
        seen.add(c)
        pick.append(c)
        if len(pick) == 3:
            break
    assert len(pick) == 3, (q, correct, cands)
    chs = pick + [correct]
    rnd.shuffle(chs)
    return {"q": q, "c": chs, "a": chs.index(correct), "e": e}


def mcq_len(q, correct, cands, e, rnd, shuffle=True):
    """Lengths in quarters -> choices like '2 1/2 in'. Lengths of 0 or less are dropped."""
    cands = [c for c in cands if c is not None and c > 0 and c != correct]
    if shuffle:
        cands = cands[:]
        rnd.shuffle(cands)
    return mcq(q, ch(correct), [ch(c) for c in cands], e, rnd)


def mcq_n(q, correct, cands, e, rnd):
    cands = [c for c in cands if c is not None and c > 0 and c != correct]
    return mcq(q, correct, cands, e, rnd)


def fig(svg):
    return "<div class='qfig'>" + svg + "</div>"


def svg_wrap(w, h, body, label):
    return ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 %d %d' width='%d' height='%d' "
            "role='img' aria-label='%s'>%s</svg>" % (w, h, w, h, label, body))


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


def svg_num(x, y, q, fs=16, color=INK):
    """Mixed number centered on x with baseline y; the fraction part is drawn small and stacked.
    Returns (svg, half width)."""
    w, r = divmod(q, 4)
    fs2 = int(round(fs * 0.74))
    cw = 0.6 * fs
    ws = str(w) if (w or not r) else ""
    ww = len(ws) * cw
    fw = (0.62 * fs2 + 4) if r else 0
    gap = 2 if (ws and r) else 0
    tot = ww + gap + fw
    x0 = x - tot / 2
    s = []
    if ws:
        s.append("<text x='%.1f' y='%.1f' font-size='%d' font-weight='700' fill='%s'>%s</text>" % (x0, y, fs, color, ws))
    if r:
        n, d = {1: (1, 4), 2: (1, 2), 3: (3, 4)}[r]
        xf = x0 + ww + gap + fw / 2
        ym = y - 0.36 * fs
        s.append("<text x='%.1f' y='%.1f' font-size='%d' font-weight='700' fill='%s' text-anchor='middle'>%d</text>"
                 % (xf, ym - 2, fs2, color, n))
        s.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='1.3'/>"
                 % (xf - fw / 2, ym, xf + fw / 2, ym, color))
        s.append("<text x='%.1f' y='%.1f' font-size='%d' font-weight='700' fill='%s' text-anchor='middle'>%d</text>"
                 % (xf, ym + 2 + 0.72 * fs2, fs2, color, d))
    return "".join(s), tot / 2


# ------------------------------------------------------------ ruler pictures
OBJ_Y0, OBJ_Y1 = 8, 32          # band the object is drawn in
R_TOP = 40                      # top edge of the ruler


def draw_object(kind, x0, x1):
    yt, yb = OBJ_Y0, OBJ_Y1
    ym = (yt + yb) / 2
    L = x1 - x0
    s = []
    if kind == "pencil":
        s.append("<rect x='%.1f' y='%d' width='9' height='%d' fill='#f2a7b5' stroke='%s' stroke-width='1.2'/>" % (x0, yt + 2, yb - yt - 4, INK))
        s.append("<rect x='%.1f' y='%d' width='6' height='%d' fill='#b8b8b8' stroke='%s' stroke-width='1.2'/>" % (x0 + 9, yt + 1, yb - yt - 2, INK))
        s.append("<rect x='%.1f' y='%d' width='%.1f' height='%d' fill='#f4c430' stroke='%s' stroke-width='1.2'/>" % (x0 + 15, yt + 1, L - 33, yb - yt - 2, INK))
        s.append("<polygon points='%.1f,%d %.1f,%d %.1f,%.1f' fill='#e8c79a' stroke='%s' stroke-width='1.2' stroke-linejoin='round'/>"
                 % (x1 - 18, yt + 1, x1 - 18, yb - 1, x1, ym, INK))
        s.append("<polygon points='%.1f,%.1f %.1f,%.1f %.1f,%.1f' fill='%s'/>" % (x1 - 6, ym - 3.6, x1 - 6, ym + 3.6, x1, ym, INK))
    elif kind == "crayon":
        s.append("<rect x='%.1f' y='%d' width='%.1f' height='%d' rx='3' fill='#3d7cc9' stroke='%s' stroke-width='1.2'/>" % (x0, yt + 2, L - 12, yb - yt - 4, INK))
        s.append("<rect x='%.1f' y='%d' width='%.1f' height='%d' fill='#9cc3ee'/>" % (x0 + 6, yt + 8, max(L - 26, 4), yb - yt - 16))
        s.append("<polygon points='%.1f,%d %.1f,%d %.1f,%.1f %.1f,%.1f' fill='#3d7cc9' stroke='%s' stroke-width='1.2' stroke-linejoin='round'/>"
                 % (x1 - 12, yt + 4, x1 - 12, yb - 4, x1, ym + 2.5, x1, ym - 2.5, INK))
    elif kind == "leaf":
        xm = (x0 + x1) / 2
        s.append("<path d='M%.1f %.1f Q%.1f %d %.1f %.1f Q%.1f %d %.1f %.1f Z' fill='#7cc47f' stroke='%s' stroke-width='1.4'/>"
                 % (x0, ym, xm, yt - 9, x1, ym, xm, yb + 9, x0, ym, GREEN))
        s.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='1.2'/>" % (x0 + 2, ym, x1 - 3, ym, GREEN))
    elif kind == "nail":
        s.append("<rect x='%.1f' y='%d' width='4' height='%d' fill='#9aa0a6' stroke='%s' stroke-width='1.1'/>" % (x0, yt + 3, yb - yt - 6, INK))
        s.append("<polygon points='%.1f,%.1f %.1f,%.1f %.1f,%.1f %.1f,%.1f %.1f,%.1f' fill='#c3c7cb' stroke='%s' "
                 "stroke-width='1.1' stroke-linejoin='round'/>"
                 % (x0 + 4, ym - 3, x1 - 10, ym - 3, x1, ym, x1 - 10, ym + 3, x0 + 4, ym + 3, INK))
    elif kind == "ribbon":
        s.append("<rect x='%.1f' y='%d' width='%.1f' height='%d' fill='#e05a6a' stroke='%s' stroke-width='1.2'/>" % (x0, yt + 6, L, yb - yt - 12, INK))
    elif kind == "paper strip":
        s.append("<rect x='%.1f' y='%d' width='%.1f' height='%d' fill='#cfe3f7' stroke='%s' stroke-width='1.2'/>" % (x0, yt + 4, L, yb - yt - 8, INK))
    elif kind == "craft stick":
        s.append("<rect x='%.1f' y='%d' width='%.1f' height='%d' rx='8' fill='#e6c88f' stroke='%s' stroke-width='1.2'/>" % (x0, yt + 4, L, yb - yt - 8, INK))
    elif kind == "eraser":
        s.append("<rect x='%.1f' y='%d' width='%.1f' height='%d' rx='3' fill='#f2a7b5' stroke='%s' stroke-width='1.2'/>" % (x0, yt + 2, L, yb - yt - 4, INK))
    elif kind == "caterpillar":
        k = max(2, int(round(L / 15.0)))
        d = L / k
        for i in range(k):
            col = "#4e9a3f" if i == k - 1 else "#8cc63f"
            s.append("<circle cx='%.1f' cy='%.1f' r='%.1f' fill='%s' stroke='%s' stroke-width='1.1'/>"
                     % (x0 + d * (i + 0.5), ym + 2, d / 2 - 0.4, col, GREEN))
        s.append("<circle cx='%.1f' cy='%.1f' r='1.6' fill='%s'/>" % (x1 - d * 0.35, ym, INK))
    return "".join(s)


def ruler_svg(n_in, ppi, quarters, obj=None, length=0, arrow=None):
    """Ruler 0..n_in inches. obj is drawn from 0 to `length` quarters; arrow points at a mark (quarters)."""
    pad = 18
    W = int(2 * pad + n_in * ppi)
    H = R_TOP + 46
    X = lambda q: pad + ppi * q / 4.0
    s = ["<rect x='%d' y='%d' width='%d' height='%d' rx='3' fill='%s' stroke='%s' stroke-width='1.5'/>"
         % (pad - 12, R_TOP, n_in * ppi + 24, 44, RULER, INK)]
    for q in range(0, n_in * 4 + 1):
        if q % 4 == 0:
            ln, sw = 22, 2
        elif q % 2 == 0:
            ln, sw = 15, 1.6
        else:
            if not quarters:
                continue
            ln, sw = 9, 1.3
        s.append("<line x1='%.1f' y1='%d' x2='%.1f' y2='%d' stroke='%s' stroke-width='%s'/>" % (X(q), R_TOP, X(q), R_TOP + ln, INK, sw))
        if q % 4 == 0:
            s.append("<text x='%.1f' y='%d' font-size='15' font-weight='700' fill='%s' text-anchor='middle'>%d</text>"
                     % (X(q), R_TOP + 38, INK, q // 4))
    label = "ruler marked in %s" % ("quarter inches" if quarters else "half inches")
    if obj:
        s.append("<line x1='%.1f' y1='3' x2='%.1f' y2='%d' stroke='%s' stroke-width='1' stroke-dasharray='3 2'/>" % (X(0), X(0), R_TOP, GREY))
        s.append("<line x1='%.1f' y1='3' x2='%.1f' y2='%d' stroke='%s' stroke-width='1' stroke-dasharray='3 2'/>" % (X(length), X(length), R_TOP, GREY))
        s.append(draw_object(obj, X(0), X(length)))
        label = "%s above a %s" % (obj, label)
    if arrow is not None:
        x = X(arrow)
        s.append("<polygon points='%.1f,%d %.1f,%d %.1f,%d' fill='%s'/>" % (x - 8, 12, x + 8, 12, x, R_TOP - 1, RED))
        s.append("<rect x='%.1f' y='3' width='6' height='10' fill='%s'/>" % (x - 3, RED))
        label = "arrow pointing to a mark on a " + label
    return svg_wrap(W, H, "".join(s), label)


# ------------------------------------------------------------ line plots
def plot_svg(start, step, counts, label="line plot of lengths in inches", gap=46):
    n = len(counts)
    mx = max(max(counts), 1)
    pad = 30
    gap = max(gap, int(240 / (n - 1)))            # short plots get wider spacing so they print wide, not tall
    W = int(2 * pad + gap * (n - 1))
    Y = 30 + 16 * (mx - 1)
    H = Y + 60
    X = lambda i: pad + gap * i
    s = ["<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='2'/>" % (pad - 16, Y, W - pad + 16, Y, INK)]
    for i in range(n):
        x = X(i)
        s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='1.8'/>" % (x, Y - 6, x, Y + 6, INK))
        t, _ = svg_num(x, Y + 27, start + i * step, fs=16)
        s.append(t)
        for k in range(counts[i]):
            cy = Y - 18 - 16 * k
            s.append("<path d='M%d %d L%d %d M%d %d L%d %d' stroke='%s' stroke-width='2.4' stroke-linecap='round'/>"
                     % (x - 6, cy - 6, x + 6, cy + 6, x - 6, cy + 6, x + 6, cy - 6, GREEN))
    s.append("<text x='%d' y='%d' font-size='13' fill='%s' text-anchor='middle'>Length (inches)</text>" % (W / 2, Y + 53, INK))
    return svg_wrap(W, H, "".join(s), label)


# what was measured: (plural, singular, smallest, largest) in quarter inches
CTX = [("leaves", "leaf", 8, 20), ("shells", "shell", 4, 14), ("crayons", "crayon", 8, 15),
       ("pencils", "pencil", 12, 28), ("earthworms", "earthworm", 8, 20), ("feathers", "feather", 8, 24),
       ("twigs", "twig", 12, 24), ("toy cars", "toy car", 8, 16), ("erasers", "eraser", 4, 10),
       ("pine cones", "pine cone", 8, 16), ("caterpillars", "caterpillar", 4, 10), ("ribbon pieces", "ribbon piece", 4, 24),
       ("baby carrots", "baby carrot", 8, 13), ("rocks", "rock", 4, 12)]


class Ctx:
    def __init__(self, rnd):
        self.rnd = rnd
        self.pool = CTX[:]
        rnd.shuffle(self.pool)
        self.i = 0

    def next(self):
        c = self.pool[self.i % len(self.pool)]
        self.i += 1
        return c


def make_plot(rnd, ctx, ok, step=None, n=None):
    """Random line plot data inside the context's range; `ok(counts)` must be true."""
    pl, sg, lo, hi = ctx
    if step is None:
        step = rnd.choice([1, 2]) if (hi - lo) // 2 + 1 >= (n or 5) else 1
    if n is None:
        n = min(7, (hi - lo) // step + 1)
    starts = [s for s in range(lo, hi - step * (n - 1) + 1) if s % step == 0]
    for _ in range(4000):
        s = rnd.choice(starts)
        peak = rnd.randrange(n)
        counts = []
        for i in range(n):
            d = abs(i - peak)
            counts.append(max(0, rnd.choice([4, 5, 3, 4]) - d + rnd.choice([-1, 0, 0, 1])))
        counts = [min(c, 5) for c in counts]
        tot = sum(counts)
        ends_ok = not (counts[0] == 0 and counts[1] == 0) and not (counts[-1] == 0 and counts[-2] == 0)
        if 7 <= tot <= 18 and ends_ok and ok(counts):
            return s, step, counts
    raise RuntimeError("no plot for %s" % (ctx,))


def vals(s, step, counts):
    return [s + i * step for i in range(len(counts))]


def unique_max(counts):
    m = max(counts)
    return counts.count(m) == 1


# ------------------------------------------------------------ set 1: half inches
OBJ_H = [("pencil", 12, 22), ("crayon", 6, 14), ("leaf", 6, 22), ("nail", 4, 12), ("ribbon", 4, 22),
         ("paper strip", 4, 22), ("craft stick", 12, 22), ("caterpillar", 4, 10)]
OBJ_Q = [("pencil", 9, 15), ("crayon", 5, 15), ("leaf", 5, 15), ("nail", 3, 12), ("ribbon", 3, 15),
         ("paper strip", 3, 15), ("caterpillar", 3, 10), ("eraser", 5, 10)]


def half_e(obj, L):
    w, r = divmod(L, 4)
    if r == 0:
        return ("Line up the end of the %s with 0. It ends right at the long mark for %d. "
                "Count the inch spaces from 0: the %s is %s long. (Do not start counting at 1.)" % (obj, w, obj, inches(L)))
    if w == 0:
        return ("The %s starts at 0 and ends at the middle mark between 0 and 1. "
                "That mark is halfway to 1, so the %s is %s long." % (obj, obj, inches(L)))
    return ("The %s starts at 0 and ends at the middle mark between %d and %d. That mark is halfway, "
            "so the %s is %s long." % (obj, w, w + 1, obj, inches(L)))


def half_cands(L):
    w, r = divmod(L, 4)
    c = [L + 4, L - 2, L + 2, L * 2 if L % 4 else None]       # started at 1, next mark, counted half spaces as inches
    if r:
        c.append(L - 1)                                           # called the half mark a fourth
    return c


def set_half(rnd):
    its = []
    combos = [(o, L) for o, lo, hi in OBJ_H for L in range(lo, hi + 1, 2)]
    rnd.shuffle(combos)
    used_obj, used_len, picked = {}, {}, []
    want_whole = 4
    for o, L in combos:                                           # 14 objects: 10 with a half, 4 whole
        if used_obj.get(o, 0) >= 2 or used_len.get(L, 0) >= 2:
            continue
        if L % 4 == 0:
            if want_whole == 0:
                continue
            want_whole -= 1
        elif len(picked) - (4 - want_whole) >= 10:
            continue
        used_obj[o] = used_obj.get(o, 0) + 1
        used_len[L] = used_len.get(L, 0) + 1
        picked.append((o, L))
        if len(picked) == 14:
            break
    assert len(picked) == 14
    asks = ["How long is the %s?", "Measure the %s to the nearest half inch.", "How long is the %s to the nearest half inch?"]
    for i, (o, L) in enumerate(picked):
        q = fig(ruler_svg(6, 56, False, obj=o, length=L)) + (asks[i % 3] % o)
        its.append(mcq_len(q, L, half_cands(L), half_e(o, L), rnd))
    for L in rnd.sample([2, 6, 10, 14, 18, 22], 6):              # arrows at half marks
        w = L // 4
        e = ("The arrow points to the middle mark between %d and %d. That mark is halfway between them, so it shows %s." %
             (w, w + 1, inches(L)))
        its.append(mcq_len(fig(ruler_svg(6, 56, False, arrow=L)) + "The ruler is marked in half inches. "
                           "What length does the arrow point to?", L, [L - 2, L + 2, L - 1, L + 1], e, rnd))
    rnd.shuffle(its)
    return {"title": "Measure to the nearest half inch", "items": its}


# ------------------------------------------------------------ set 2: quarter inches
def quarter_e(obj, L):
    w, r = divmod(L, 4)
    base = "Each inch has 4 equal spaces, so each small space is %s inch. " % fr(1, 4)
    frm = "0" if w == 0 else str(w)
    if r == 2:
        return base + ("The %s ends 2 small spaces past %s. %s is the same as %s, so it is %s long."
                       % (obj, frm, fr(2, 4), fr(1, 2), inches(L)))
    return base + ("The %s ends %s past %s, so it is %s long."
                   % (obj, nword(r, "small space", "small spaces"), frm, inches(L)))


def quarter_cands(L):
    w, r = divmod(L, 4)
    swap = {1: L + 2, 3: L - 2}.get(r)                            # mixed up 1/4 and 3/4
    return [swap, L - 1, L + 1, L + 4, w * 4 if w else None, (w + 1) * 4]


def set_quarter(rnd):
    its = []
    combos = [(o, L) for o, lo, hi in OBJ_Q for L in range(lo, hi + 1) if L % 4]
    rnd.shuffle(combos)
    used_obj, used_len, picked = {}, {}, []
    halves = 0
    for o, L in combos:
        if used_obj.get(o, 0) >= 2 or used_len.get(L, 0) >= 2:
            continue
        if L % 4 == 2:
            if halves >= 3:
                continue
            halves += 1
        used_obj[o] = used_obj.get(o, 0) + 1
        used_len[L] = used_len.get(L, 0) + 1
        picked.append((o, L))
        if len(picked) == 14:
            break
    assert len(picked) == 14
    asks = ["How long is the %s?", "Measure the %s to the nearest quarter inch.", "How long is the %s to the nearest quarter inch?"]
    for i, (o, L) in enumerate(picked):
        q = fig(ruler_svg(4, 64, True, obj=o, length=L)) + (asks[i % 3] % o)
        its.append(mcq_len(q, L, quarter_cands(L), quarter_e(o, L), rnd))
    arr = rnd.sample([1, 3, 5, 7, 9, 11, 13, 15], 5) + [10]
    for L in arr:
        w, r = divmod(L, 4)
        e = ("Each small space is %s inch. The arrow is %s past %d, so it shows %s."
             % (fr(1, 4), nword(r, "small space", "small spaces"), w, inches(L)))
        if r == 2:
            e += " %s is the same as %s." % (fr(2, 4), fr(1, 2))
        its.append(mcq_len(fig(ruler_svg(4, 64, True, arrow=L)) + "The ruler is marked in quarter inches. "
                           "What length does the arrow point to?", L, quarter_cands(L), e, rnd))
    rnd.shuffle(its)
    return {"title": "Measure to the nearest quarter inch", "items": its}


# ------------------------------------------------------------ set 3: read a line plot
def intro(P, T, ctx, rnd):
    pl = ctx[0]
    if rnd.random() < 0.5:
        n, he, his = P.next()
        return "%s measured some %s. The line plot shows the lengths." % (n, pl), (n, he)
    t = T[rnd.randrange(len(T))]
    return "%s's class measured some %s. The line plot shows the lengths." % (t, pl), ("the class", "they")


def set_read(rnd, P, C):
    its = []
    for kind in ["count", "most", "total", "longest"] * 5:
        ctx = C.next()
        pl, sg = ctx[0], ctx[1]
        if kind == "count":
            s, st, cn = make_plot(rnd, ctx, lambda c: c[0] > 0 and min(c) >= 0)
            V = vals(s, st, cn)
            idx = [i for i in range(len(cn)) if cn[i] >= 2 and 0 < i < len(cn) - 1]
            i = rnd.choice(idx) if idx else max(range(len(cn)), key=lambda k: cn[k])
            v, c = V[i], cn[i]
            txt, who = intro(P, TEACHERS, ctx, rnd)
            q = fig(plot_svg(s, st, cn)) + txt + " How many %s are %s long?" % (pl, inches(v))
            cand = [cn[i - 1] if i > 0 else None, cn[i + 1] if i + 1 < len(cn) else None, sum(cn), c + 1, c - 1]
            e = ("Find %s on the number line. Count only the X's in that column: %d. "
                 "Do not count the X's above the marks next to it." % (num(v), c))
            its.append(mcq_n(q, c, cand, e, rnd))
        elif kind == "most":
            s, st, cn = make_plot(rnd, ctx, lambda c: unique_max(c) and c.index(max(c)) != len(c) - 1 and c[-1] > 0)
            V = vals(s, st, cn)
            m = cn.index(max(cn))
            order = sorted(range(len(cn)), key=lambda k: -cn[k])
            second = order[1]
            last = max(k for k in range(len(cn)) if cn[k])
            first = min(k for k in range(len(cn)) if cn[k])
            txt, who = intro(P, TEACHERS, ctx, rnd)
            q = fig(plot_svg(s, st, cn)) + txt + " Which length is the most common?"
            e = "The most common length has the tallest stack of X's. The stack above %s has %d X's, more than any other." % (num(V[m]), cn[m])
            its.append(mcq_len(q, V[m], [V[second], V[last], V[first], V[m] + st, V[m] - st], e, rnd, shuffle=False))
        elif kind == "total":
            s, st, cn = make_plot(rnd, ctx, lambda c: True)
            tot = sum(cn)
            cols = sum(1 for x in cn if x)
            txt, who = intro(P, TEACHERS, ctx, rnd)
            if who[0] == "the class":
                ask = " How many %s did the class measure in all?" % pl
            else:
                ask = " How many %s did %s measure in all?" % (pl, who[0])
            q = fig(plot_svg(s, st, cn)) + txt + ask
            e = ("Each X is one %s. Add the X's in every column: %s = %d." %
                 (sg, " + ".join(str(x) for x in cn if x), tot))
            its.append(mcq_n(q, tot, [len(cn), cols, max(cn), tot - 1, tot + 1], e, rnd))
        else:
            s, st, cn = make_plot(rnd, ctx, lambda c: c[-1] == 0 and c[-2] > 0 and c[0] > 0 and unique_max(c)
                                  and c.index(max(c)) != len(c) - 2)
            V = vals(s, st, cn)
            last = max(k for k in range(len(cn)) if cn[k])
            m = cn.index(max(cn))
            txt, who = intro(P, TEACHERS, ctx, rnd)
            q = fig(plot_svg(s, st, cn)) + txt + " How long is the longest %s?" % sg
            e = ("Look for the X that is farthest to the right: it is above %s. "
                 "The mark %s has no X, so no %s is that long." % (num(V[last]), num(V[-1]), sg))
            its.append(mcq_len(q, V[last], [V[-1], V[m], V[last] - st], e, rnd, shuffle=False))
    return {"title": "Read a line plot", "items": its}


# ------------------------------------------------------------ set 4: compare data on a line plot
def count_up_e(lo, hi):
    """Explain hi - lo by counting up from lo (whole inches first, then the part)."""
    D = hi - lo
    w, r = divmod(D, 4)
    steps = []
    if w:
        steps.append("from %s to %s is %s" % (num(lo), num(lo + 4 * w), nword(w, "inch", "inches")))
    if r:
        steps.append("from %s to %s is %s inch more" % (num(lo + 4 * w), num(hi), num(r)) if w else
                     "from %s to %s is %s inch" % (num(lo), num(hi), num(r)))
    return "Count up from the shortest: " + ", then ".join(steps) + ". The difference is %s." % inches(D)


def set_compare(rnd, P, C):
    its = []
    for kind in ["more", "longer", "or", "diff", "more"] * 4:
        ctx = C.next()
        pl, sg = ctx[0], ctx[1]
        txt, who = intro(P, TEACHERS, ctx, rnd)
        if kind == "more":
            s, st, cn = make_plot(rnd, ctx, lambda c: max(c) - min(x for x in c if x) >= 2)
            V = vals(s, st, cn)
            hiI = cn.index(max(cn))
            lows = [k for k in range(len(cn)) if 0 < cn[k] <= cn[hiI] - 2]
            loI = rnd.choice(lows)
            a, b = cn[hiI], cn[loI]
            q = fig(plot_svg(s, st, cn)) + txt + " How many more %s are %s long than %s long?" % (pl, inches(V[hiI]), inches(V[loI]))
            e = ("%s has %s. %s has %s. %d − %d = %d more."
                 % (num(V[hiI]), nword(a, "X", "X's"), num(V[loI]), nword(b, "X", "X's"), a, b, a - b))
            its.append(mcq_n(q, a - b, [a + b, a, b, a - b + 1, a - b - 1], e, rnd))
        elif kind == "longer":
            s, st, cn = make_plot(rnd, ctx, lambda c: True)
            V = vals(s, st, cn)
            opts = [k for k in range(1, len(cn) - 1) if cn[k] > 0 and sum(cn[k + 1:]) > 0]
            k = rnd.choice(opts)
            ans = sum(cn[k + 1:])
            q = fig(plot_svg(s, st, cn)) + txt + " How many %s are longer than %s?" % (pl, inches(V[k]))
            right = [x for x in cn[k + 1:] if x]
            e = ("Longer means to the right of %s. Do not count the X's above %s itself. " % (num(V[k]), num(V[k])) +
                 ("Add the X's to the right: %s = %d." % (" + ".join(str(x) for x in right), ans) if len(right) > 1
                  else "Only one column to the right has X's: %s." % nword(ans, "X", "X's")))
            its.append(mcq_n(q, ans, [ans + cn[k], cn[k + 1], sum(cn[:k]), sum(cn[:k + 1]), ans + 1, ans - 1], e, rnd))
        elif kind == "or":
            s, st, cn = make_plot(rnd, ctx, lambda c: sum(1 for x in c if x >= 2) >= 2)
            V = vals(s, st, cn)
            ks = rnd.sample([k for k in range(len(cn)) if cn[k] >= 2], 2)
            i, j = sorted(ks)
            a, b = cn[i], cn[j]
            q = fig(plot_svg(s, st, cn)) + txt + " How many %s are either %s or %s long?" % (pl, inches(V[i]), inches(V[j]))
            e = "Count the X's above %s: %d. Count the X's above %s: %d. Add them: %d + %d = %d." % (
                num(V[i]), a, num(V[j]), b, a, b, a + b)
            its.append(mcq_n(q, a + b, [abs(a - b), a, b, sum(cn), a + b + 1], e, rnd))
        else:
            s, st, cn = make_plot(rnd, ctx, lambda c: True)
            V = vals(s, st, cn)
            first = min(k for k in range(len(cn)) if cn[k])
            last = max(k for k in range(len(cn)) if cn[k])
            lo, hi = V[first], V[last]
            D = hi - lo
            spaces = last - first
            q = (fig(plot_svg(s, st, cn)) + txt +
                 " How much longer is the longest %s than the shortest %s?" % (sg, sg))
            e = "Longest: %s. Shortest: %s. " % (inches(hi), inches(lo)) + count_up_e(lo, hi)
            its.append(mcq_len(q, D, [spaces * 4, (spaces + 1) * st, hi, D + st, D - st], e, rnd, shuffle=False))
    return {"title": "Compare data on a line plot", "items": its}


# ------------------------------------------------------------ set 5: word problems
def data_list(rnd, s, st, cn):
    d = []
    for i, c in enumerate(cn):
        d += [s + i * st] * c
    rnd.shuffle(d)
    return d


def list_html(d):
    return ", ".join(num(v) for v in d)


def set_story(rnd, P, C):
    its = []
    # A: one X is missing
    for _ in range(5):
        ctx = C.next()
        pl, sg = ctx[0], ctx[1]
        s, st, cn = make_plot(rnd, ctx, lambda c: c[0] > 0 and c[-1] > 0 and sum(c) <= 11, n=5)
        V = vals(s, st, cn)
        d = data_list(rnd, s, st, cn)
        k = rnd.choice([i for i in range(len(cn)) if cn[i] >= 1])
        shown = cn[:]
        shown[k] -= 1
        n, he, his = P.next()
        q = (fig(plot_svg(s, st, shown)) +
             "%s measured %d %s. The lengths in inches are: %s. %s made this line plot but forgot one X. "
             "Where does the missing X go?" % (n, len(d), pl, list_html(d), cap(he)))
        e = ("Count how many times each length is in the list. %s is in the list %s, "
             % (num(V[k]), "once" if cn[k] == 1 else "%d times" % cn[k]) +
             ("but the plot has no X above it. " if shown[k] == 0 else
              "but the plot shows only %s above it. " % nword(shown[k], "X", "X's")) +
             "The missing X goes above %s." % num(V[k]))
        top = shown.index(max(shown))
        cand = [V[top], V[k] + st if k + 1 < len(cn) else None, V[k] - st if k > 0 else None, V[(k + 2) % len(V)]] + V
        its.append(mcq_len(q, V[k], cand, e, rnd, shuffle=False))
    # B: one more measurement
    for _ in range(5):
        ctx = C.next()
        pl, sg = ctx[0], ctx[1]
        s, st, cn = make_plot(rnd, ctx, lambda c: True)
        V = vals(s, st, cn)
        k = rnd.choice([i for i in range(1, len(cn) - 1) if cn[i] >= 1])
        n, he, his = P.next()
        q = (fig(plot_svg(s, st, cn)) +
             "%s made this line plot of %s lengths. Then %s measured one more %s. It is %s long. "
             "How many X's will be above %s now?" % (n, sg, he, sg, inches(V[k]), num(V[k])))
        e = "%s above %s now. Add 1 X for the new %s: %d + 1 = %d." % (
            "There is 1 X" if cn[k] == 1 else "There are %d X's" % cn[k], num(V[k]), sg, cn[k], cn[k] + 1)
        its.append(mcq_n(q, cn[k] + 1, [cn[k], cn[k] + 2, cn[k + 1] + 1, sum(cn) + 1], e, rnd))
    # C: from a list (no picture)
    for j in range(5):
        ctx = C.next()
        pl, sg = ctx[0], ctx[1]
        s, st, cn = make_plot(rnd, ctx, lambda c: unique_max(c) and sum(c) <= 10 and sum(1 for x in c if x) >= 4,
                              n=5 if ctx[3] - ctx[2] >= 8 else None)
        V = vals(s, st, cn)
        d = data_list(rnd, s, st, cn)
        t = TEACHERS[j % len(TEACHERS)]
        head = "%s's class measured %d %s. The lengths in inches are: %s. " % (t, len(d), pl, list_html(d))
        if j < 3:
            k = rnd.choice([i for i in range(len(cn)) if cn[i] >= 2])
            q = head + "On a line plot of this data, how many X's go above %s?" % num(V[k])
            e = ("Put 1 X for each length in the list. %s appears %d times in the list, so it gets %d X's."
                 % (num(V[k]), cn[k], cn[k]))
            nb = [cn[i] for i in (k - 1, k + 1) if 0 <= i < len(cn)]
            its.append(mcq_n(q, cn[k], nb + [cn[k] + 1, cn[k] - 1, len(d)], e, rnd))
        else:
            m = cn.index(max(cn))
            q = head + "On a line plot of this data, which length will have the most X's?"
            e = ("Count each length in the list. %s appears %s, more than any other length, "
                 "so it gets the tallest stack of X's." % (num(V[m]), nword(cn[m], "time", "times")))
            others = sorted([i for i in range(len(cn)) if i != m and cn[i]], key=lambda i: -cn[i])
            its.append(mcq_len(q, V[m], [V[i] for i in others] + [max(d), d[0]], e, rnd, shuffle=False))
    # D: choosing the scale
    n, he, his = P.next()
    d = [6, 7, 9, 6, 10, 7, 11, 9]
    q = ("%s measured 8 crayons. The lengths in inches are: %s. Which scale on the line plot has a mark for every length?"
         % (n, list_html(d)))
    e = ("Some lengths, like %s and %s, end in fourths. A line plot needs a mark for each one, "
         "so the number line must be marked in quarter inches." % (num(7), num(11)))
    its.append(mcq(q, "quarter inches", ["half inches", "whole inches", "every 2 inches"], e, rnd))
    n, he, his = P.next()
    q = ("%s measured 4 shells: %s, 3, %s and 4 inches. %s makes a line plot marked in half inches: "
         "2, %s, 3, %s, 4. Which length has no mark on this line plot?"
         % (n, num(10), num(11), cap(he), num(10), num(14)))
    e = ("Half-inch marks are whole numbers and halves. %s ends in a fourth, so it falls between "
         "%s and 3. It needs a line plot marked in quarter inches." % (num(11), num(10)))
    its.append(mcq(q, ch(11), [ch(10), ch(12), ch(16)], e, rnd))
    # E: longest - shortest from a list
    used_d = set()
    for nt in (4, 6, 5):
        ctx = C.next()
        pl, sg = ctx[0], ctx[1]
        for _try in range(500):
            s, st, cn = make_plot(rnd, ctx, lambda c: c[0] > 0 and c[-1] > 0 and sum(c) <= 10, n=nt)
            V = vals(s, st, cn)
            d = data_list(rnd, s, st, cn)
            lo, hi = min(d), max(d)
            fl = abs(d[0] - d[-1])
            if fl not in (0, hi - lo) and d[0] not in (lo, hi) and hi - lo not in used_d:
                break
        else:
            raise RuntimeError("no list for longest - shortest")
        used_d.add(hi - lo)
        n, he, his = P.next()
        q = ("%s measured %d %s. The lengths in inches are: %s. How much longer is the longest %s than the shortest %s?"
             % (n, len(d), pl, list_html(d), sg, sg))
        e = ("Find the longest, %s, and the shortest, %s. Do not just use the first and last numbers in the list. "
             % (inches(hi), inches(lo)) + count_up_e(lo, hi))
        D = hi - lo
        its.append(mcq_len(q, D, [fl, (D // st) * 4, D + st, D - st, hi], e, rnd, shuffle=False))
    return {"title": "Word problems: make and use line plots", "items": its}


# ------------------------------------------------------------ lesson
def ex(title, q, s, a):
    return ("<div class='sn-ex'><span class='sn-ex-t'>%s</span><p class='sn-ex-q'>%s</p>"
            "<p class='sn-ex-s'>%s</p><p class='sn-ex-a'>Answer: %s</p></div>" % (title, q, s, a))


def table(head, rows):
    h = "".join("<th>%s</th>" % x for x in head)
    b = "".join("<tr>" + "".join("<td>%s</td>" % c for c in r) + "</tr>" for r in rows)
    return "<div class='sn-tw'><table class='sn-table'><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>" % (h, b)


LESSON_DATA = [8, 9, 9, 10, 10, 10, 11, 12, 12, 13]       # 2 to 3 1/4 inches, in quarters
LESSON_COUNTS = [1, 2, 3, 1, 2, 1]                         # same data counted from 2 by quarters


def body_html():
    assert sorted(LESSON_DATA) == [8 + i for i, c in enumerate(LESSON_COUNTS) for _ in range(c)]
    return (
        "<h2>Measure with a ruler</h2>"
        "<p>Put the end of the object at <b>0</b>. Look straight down from the other end and read the mark. "
        "A length is the number of <b>spaces</b> from 0, not the number of marks.</p>"
        "<figure class='sn-fig'>" + ruler_svg(6, 56, False, obj="pencil", length=14) +
        "<figcaption>The pencil starts at 0 and ends at the middle mark between 3 and 4. It is 3 " + fr(1, 2) +
        " inches long.</figcaption></figure>"
        "<h2>Halves and fourths of an inch</h2>"
        "<p>The marks on a ruler have different lengths. The longer the mark, the bigger the part it shows.</p>" +
        table(["Mark", "What it shows", "Examples"], [
            ["Long mark with a number", "Whole inches", "1, 2, 3"],
            ["Middle mark", "Half inches", fr(1, 2) + ", 1 " + fr(1, 2) + ", 2 " + fr(1, 2)],
            ["Short mark", "Quarter inches (fourths)", fr(1, 4) + ", " + fr(3, 4) + ", 2 " + fr(1, 4)],
        ]) +
        "<figure class='sn-fig'>" + ruler_svg(4, 64, True, obj="crayon", length=11) +
        "<figcaption>Each inch has 4 small spaces, so each space is " + fr(1, 4) + " inch. The crayon ends 3 spaces past 2. "
        "It is 2 " + fr(3, 4) + " inches long.</figcaption></figure>" +
        ex("Example", "A ruler is marked in quarter inches. A nail ends 2 small spaces past 1. How long is it?",
           "2 small spaces = " + fr(2, 4) + " inch, which is the same as " + fr(1, 2) + " inch. So the nail is 1 " + fr(1, 2) + " inches.",
           "1 " + fr(1, 2) + " inches") +
        "<h2>Make a line plot</h2>"
        "<p>A line plot shows many measurements at once. Draw a number line with marks that fit the data: "
        "whole numbers, halves or quarters. Then put <b>one X</b> above the mark for each measurement.</p>"
        "<p>A class measured 10 leaves. The lengths in inches are: " + list_html(LESSON_DATA) + ".</p>"
        "<figure class='sn-fig'>" + plot_svg(8, 1, LESSON_COUNTS, label="line plot of 10 leaf lengths") +
        "<figcaption>The data has fourths, so the number line is marked in quarter inches. There are 10 X's for 10 leaves.</figcaption></figure>"
        "<h2>Read a line plot</h2>" +
        table(["Question", "How to find it", "Answer"], [
            ["How many leaves are 2 " + fr(1, 2) + " inches long?", "Count the X's above 2 " + fr(1, 2), "3"],
            ["Which length is most common?", "Find the tallest stack", "2 " + fr(1, 2) + " in"],
            ["How many leaves in all?", "1 + 2 + 3 + 1 + 2 + 1", "10"],
            ["How many more leaves are 2 " + fr(1, 2) + " inches than 2 inches?", "3 − 1", "2"],
        ]) +
        ex("Example", "How much longer is the longest leaf than the shortest leaf?",
           "Longest: 3 " + fr(1, 4) + " in. Shortest: 2 in. Count up: from 2 to 3 is 1 inch, then from 3 to 3 " + fr(1, 4) +
           " is " + fr(1, 4) + " inch more.", "1 " + fr(1, 4) + " inches") +
        "<h2>Common mistakes</h2>" +
        table(["Mistake", "What to do instead"], [
            ["Starting the object at the end of the ruler or at 1", "Line up the end of the object with 0"],
            ["Counting tick marks", "Count the spaces between marks"],
            ["Calling a short mark a half", "Middle marks are halves. Short marks are fourths"],
            ["Reading the last number on the line plot as the longest", "The longest is the X farthest to the right"],
            ["Counting the X's in the column next to it", "Point to the mark, then count straight up"],
        ])
    )


FAQ = [
    {"q": "What is a line plot in 3rd grade math?",
     "a": "A line plot is a number line with an X above it for each measurement. In 3rd grade, students measure lengths to the nearest half or quarter inch and show the data on a line plot."},
    {"q": "How do you measure to the nearest quarter inch?",
     "a": "Line up the end of the object with 0. Each inch has 4 small spaces, each worth 1/4 inch. Read the whole inch, then count the small spaces past it, such as 2 and 3/4 inches."},
    {"q": "How do you make a line plot with fractions?",
     "a": "Draw a number line marked in halves or fourths so every measurement has a mark. Then put one X above the mark for each measurement, stacking the X's when lengths repeat."},
    {"q": "Which marks on a ruler show half and quarter inches?",
     "a": "The long numbered marks are whole inches. The middle mark between two numbers is the half inch, and the shortest marks are the quarter inches."},
]


def gen_line_plots():
    rnd = random.Random(41)
    P = People(rnd)
    C = Ctx(rnd)
    sets = [set_half(rnd), set_quarter(rnd), set_read(rnd, P, C), set_compare(rnd, P, C), set_story(rnd, P, C)]
    seen = set()
    for s in sets:
        assert len(s["items"]) == 20, (s["title"], len(s["items"]))
        for it in s["items"]:
            assert len(set(it["c"])) == 4, it
            assert it["q"] not in seen, it["q"]
            seen.add(it["q"])
    return {
        "country": "us", "subject": "math", "grade": "grade-3", "slug": "line-plots-measurement", "sort": 11,
        "updated": UPDATED, "pdf_url": "",
        "title": "Measure to the Nearest Half and Quarter Inch and Make Line Plots",
        "seo_title": "Grade 3 Line Plot Worksheets: Measure to the Nearest Half and Quarter Inch, Read and Make Line Plots",
        "short_title": "Line Plots and Measuring",
        "domain": "Measurement and Data",
        "standard_code": "3.MD.B.4",
        "standard_url": "https://www.thecorestandards.org/Math/Content/3/MD/B/4/",
        "standard_text": "Generate measurement data by measuring lengths using rulers marked with halves and fourths of an inch. Show the data by making a line plot, where the horizontal scale is marked off in appropriate units— whole numbers, halves, or quarters.",
        "meta_desc": "Free Grade 3 line plot worksheets with pictures: measure to the nearest half and quarter inch with a ruler, read line plots, compare data and solve word problems. 100 practice questions with answers.",
        "key_big": "Start at 0 and count spaces. Put one X above each length.",
        "key_sub": "Long marks are inches, middle marks are halves, short marks are quarters. On a line plot, each X is one measurement, and the tallest stack is the most common length.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }


def mark_large(u, pattern):
    """Tag pictures that must print larger (graphs, rulers, A-D choices) so their labels stay readable."""
    rx = re.compile(r"<svg (?=[^>]*aria-label='" + pattern + ")")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u


if __name__ == "__main__":
    u = gen_line_plots()
    path = os.path.join(OUT, "line-plots-measurement.json")
    with open(path, "w", encoding="utf-8") as f:
        mark_large(u, "(line plot|arrow pointing|[a-z ]+above a ruler|[a-z ]+ruler)")
        json.dump(u, f, ensure_ascii=False, indent=1)
    print("wrote", path)
