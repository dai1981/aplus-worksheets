# -*- coding: utf-8 -*-
"""
US Grade 2 Math: Length Word Problems and Number Lines (2.MD.B.5, 2.MD.B.6)
  python tools/gen_us_math_g2_length_problems.py
Numbers as lengths on a number line, sums and differences as jumps, and length stories
(join, take away, compare, missing start or change, two steps). Every story uses ONE unit.
Every answer, jump and mark position is computed and checked in code.
HTML attributes use single quotes (no backslashes in the JSON).
"""
import json, os, random, re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "us", "math", "grade-2")
UPDATED = "2026-11-02"
GREEN = "#006633"
FILL = "#cfe6d6"
PINK = "#f6d5d1"
INK = "#2b2b2b"
RED = "#c0392b"
GREY = "#8a8a8a"
FONT = "Arial, Helvetica, sans-serif"
BOX = "☐"
GIRLS = ["Maya", "Ava", "Mia", "Zoe", "Lily", "Emma", "Nora", "Ruby", "Sofia", "Grace"]
BOYS = ["Leo", "Noah", "Eli", "Sam", "Ben", "Omar", "Kai", "Jack", "Luis", "Owen"]

# unit key -> (one, many, short label for pictures)
UNITS = {"cm": ("centimeter", "centimeters", "cm"), "in": ("inch", "inches", "in."),
         "ft": ("foot", "feet", "ft"), "m": ("meter", "meters", "m")}
OTHER = {"cm": "in", "in": "cm", "ft": "m", "m": "ft"}       # the unit a child might write by mistake


# ------------------------------------------------------------ helpers
def U(n, u):
    one, many, _ = UNITS[u]
    return "%d %s" % (n, one if n == 1 else many)


def S(n, u):
    """Short form for pictures: 25 cm, 30 in., 12 ft."""
    return "%d %s" % (n, UNITS[u][2])


def mcq(q, correct, cands, e, fixed=False):
    """4 choices: correct + the first 3 unique distractors (no number under 2 or over 100)."""
    correct = str(correct)
    seen = {correct}
    pick = []
    for c in cands:
        c = str(c)
        lead = c.split(" ")[0]
        if c in seen or not c:
            continue
        if lead.lstrip("-").isdigit() and (int(lead) < 2 or int(lead) > 100):
            continue
        seen.add(c)
        pick.append(c)
        if len(pick) == 3:
            break
    assert len(pick) == 3, (q, correct, cands)
    return {"q": q, "c": [correct] + pick, "a": 0, "e": e}


def mcq_fixed(q, letter, e):
    return {"q": q, "c": ["A", "B", "C", "D"], "a": "ABCD".index(letter), "e": e, "fixed": True}


def balance(sets, rnd):
    """Spread the correct answers evenly (5/5/5/5) in every set. A to D picture questions keep their letter."""
    for s in sets:
        need = {0: 5, 1: 5, 2: 5, 3: 5}
        for it in s["items"]:
            if it.get("fixed"):
                need[it["a"]] -= 1
        targets = [k for k in range(4) for _ in range(need[k])]
        assert all(v >= 0 for v in need.values()), need
        rnd.shuffle(targets)
        free = [it for it in s["items"] if not it.get("fixed")]
        for it, t in zip(free, targets):
            c = it["c"]
            right = c[it["a"]]
            wrong = [x for i, x in enumerate(c) if i != it["a"]]
            rnd.shuffle(wrong)
            it["c"] = wrong[:t] + [right] + wrong[t:]
            it["a"] = t
        for it in s["items"]:
            it.pop("fixed", None)


class People:
    def __init__(self, rnd):
        self.pool = [(n, "she", "her") for n in GIRLS] + [(n, "he", "his") for n in BOYS]
        rnd.shuffle(self.pool)
        self.i = 0

    def next(self):
        p = self.pool[self.i % len(self.pool)]
        self.i += 1
        return p

    def one(self):
        n, he, his = self.next()
        return dict(N=n, he=he, He=cap(he), his=his, His=cap(his), him="her" if he == "she" else "him")

    def two(self):
        a = self.next()
        b = self.next()
        return dict(A=a[0], B=b[0], heA=a[1], HeA=cap(a[1]), hisA=a[2], heB=b[1], HeB=cap(b[1]))


def cap(s):
    return s[0].upper() + s[1:]


def say(t, p, **k):
    d = dict(p)
    d.update(k)
    return t.format(**d)


def fig(svg):
    return "<div class='qfig'>" + svg + "</div>"


def svg_wrap(w, h, body, label):
    return ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 %d %d' width='%d' height='%d' "
            "role='img' aria-label='%s'><g font-family='%s'>%s</g></svg>" % (w, h, w, h, label, FONT, body))


def tw(t, fs):
    """Approximate width in px of bold Arial text."""
    return len(str(t)) * fs * 0.6


def text(x, y, t, fs=16, anchor="middle", col=INK):
    return ("<text x='%.1f' y='%.1f' font-size='%d' font-weight='700' fill='%s' text-anchor='%s'>%s</text>"
            % (x, y, fs, col, anchor, t))


def carry(a, b):
    return a % 10 + b % 10 >= 10


def borrow(a, b):
    return a % 10 < b % 10


def sub_err(a, b):
    """Subtracted the smaller ones digit from the bigger one (52 − 27 -> 35)."""
    return (a // 10 - b // 10) * 10 + abs(a % 10 - b % 10)


def add_wrong(a, b):
    s = a + b
    w = []
    if carry(a, b):
        w.append(s - 10)                    # forgot to regroup the ten
    w.append(abs(a - b))                    # subtracted instead
    w += [s + 10, s - 1, s + 1, s - 10]
    return w


def sub_wrong(a, b):
    d = a - b
    w = []
    if borrow(a, b):
        w.append(sub_err(a, b))             # smaller digit from bigger digit
    w.append(a + b)                         # added instead
    w += [d + 10, d - 10, d + 1, d - 1]
    return w


def add_e(a, b):
    s = a + b
    if a % 10 and b % 10 and b > 10:
        return "%d + %d = %d. Then %d + %d = %d." % (a, b // 10 * 10, a + b // 10 * 10, a + b // 10 * 10, b % 10, s)
    return "%d + %d = %d." % (a, b, s)


def sub_e(a, b):
    d = a - b
    if b % 10 and b > 10:
        m = a - b // 10 * 10
        return "%d − %d = %d. Then %d − %d = %d." % (a, b // 10 * 10, m, m, b % 10, d)
    return "%d − %d = %d." % (a, b, d)


def solve_box(eq, v):
    l, r = eq.replace("−", "-").replace(BOX, str(v)).split(" = ")
    return eval(l) == eval(r)


def mark_large(u, pattern):
    """Tag pictures that must print larger so their labels stay readable."""
    rx = re.compile(r"<svg (?=[^>]*aria-label='[^']*" + pattern + ")")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u


# ------------------------------------------------------------ objects drawn above a number line
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
    elif kind == "caterpillar":
        k = max(2, int(round(L / 15.0)))
        d = L / k
        for i in range(k):
            col = "#4e9a3f" if i == k - 1 else "#8cc63f"
            s.append("<circle cx='%.1f' cy='%.1f' r='%.1f' fill='%s' stroke='%s' stroke-width='1.1'/>"
                     % (x0 + d * (i + 0.5), ym + 2, d / 2 - 0.4, col, GREEN))
        s.append("<circle cx='%.1f' cy='%.1f' r='1.6' fill='%s'/>" % (x1 - d * 0.35, ym, INK))
    else:
        raise ValueError(kind)
    return "".join(s)


# ------------------------------------------------------------ number line (equally spaced points)
def nl_svg(lo, hi, px, label, lab_every=10, extra=(), dots=(), arcs=(), obj=None):
    """Number line from lo to hi with a mark at every whole number (px apart).
    extra: [(value, text, color)] labels that win over the regular ones; dots: [(value, color)];
    arcs: [(from, to, text)] jumps drawn above the line; obj: (kind, from, to) drawn above the line."""
    m, fs = 28, 15
    W = int(2 * m + (hi - lo) * px + 0.99)
    X = lambda v: m + (v - lo) * px
    top = 6
    if arcs:
        ry = max(min(26, min(abs(b - a) for a, b, _ in arcs) * px / 2.0 + 6), 16)
        top = ry + 26
    if obj:
        top = max(top, 40)
    ly = int(top + 6)
    H = ly + 30
    s = ["<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='2.2'/>" % (m - 18, ly, W - m + 18, ly, INK)]
    s.append("<polygon points='%d,%d %d,%d %d,%d' fill='%s'/>" % (m - 22, ly, m - 13, ly - 5, m - 13, ly + 5, INK))
    s.append("<polygon points='%d,%d %d,%d %d,%d' fill='%s'/>" % (W - m + 22, ly, W - m + 13, ly - 5, W - m + 13, ly + 5, INK))
    for v in range(lo, hi + 1):
        h, sw = (8, 2) if v % 10 == 0 else (6, 1.6) if v % 5 == 0 else (4, 1.3)
        s.append("<line x1='%.1f' y1='%d' x2='%.1f' y2='%d' stroke='%s' stroke-width='%s'/>" % (X(v), ly - h, X(v), ly + h, INK, sw))
    labs = {}
    for v, t, col in extra:
        labs[v] = (t, col)
    for v in range(lo, hi + 1):
        if v % lab_every or v in labs:
            continue
        ok = all(abs(X(v) - X(e)) >= (tw(v, fs) + tw(labs[e][0], fs)) / 2 + 10 for e in labs if labs[e][1] != INK)
        if ok:
            labs[v] = (str(v), INK)
    for v, (t, col) in labs.items():
        s.append(text(X(v), ly + 25, t, fs, col=col))
    if obj:
        kind, a, b = obj
        for v in (a, b):
            s.append("<line x1='%.1f' y1='%d' x2='%.1f' y2='%d' stroke='%s' stroke-width='1' stroke-dasharray='3 2'/>"
                     % (X(v), ly - 36, X(v), ly - 1, GREY))
        s.append(draw_object(kind, X(a), X(b), ly - 36, ly - 12))
    for a, b, t in arcs:
        x1, x2 = X(a), X(b)
        r = min(26, abs(x2 - x1) / 2.0 + 6) if abs(x2 - x1) < 40 else 26
        r = max(r, 16)
        s.append("<path d='M %.1f %d C %.1f %.1f %.1f %.1f %.1f %d' fill='none' stroke='%s' stroke-width='2.5'/>"
                 % (x1, ly - 2, x1, ly - r * 1.33, x2, ly - r * 1.33, x2, ly - 2, GREEN))
        s.append("<polyline points='%.1f,%d %.1f,%d %.1f,%d' fill='none' stroke='%s' stroke-width='2.5' "
                 "stroke-linejoin='round'/>" % (x2 - 5, ly - 11, x2, ly - 2, x2 + 5, ly - 11, GREEN))
        s.append(text((x1 + x2) / 2, ly - r - 6, t, 15, col=RED if "?" in t else GREEN))
    for v, col in dots:
        s.append("<circle cx='%.1f' cy='%d' r='5.5' fill='%s' stroke='white' stroke-width='1.5'/>" % (X(v), ly, col))
    return svg_wrap(W, H, "".join(s), label)


def window(a, b, maxspan=40):
    lo = min(a, b) // 10 * 10
    hi = -(-max(a, b) // 10) * 10
    if hi == max(a, b):
        hi = hi                         # the end may sit on the last big mark
    assert hi - lo <= maxspan, (a, b)
    return lo, hi


def px_for(span):
    return 13 if span <= 20 else 10 if span <= 30 else 8


def jump_svg(start, jumps, end_text=None, start_text=None, label_jumps=None, dot_end=True):
    pts = [start]
    for j in jumps:
        pts.append(pts[-1] + j)
    lo, hi = window(min(pts), max(pts))
    labs = label_jumps or [("+%d" % j) if j > 0 else ("−%d" % -j) for j in jumps]
    arcs = [(pts[k], pts[k + 1], labs[k]) for k in range(len(jumps))]
    extra = [(start, start_text or str(start), GREEN)]
    if end_text:
        extra.append((pts[-1], end_text, RED))
    dots = [(start, GREEN)] + ([(pts[-1], RED)] if dot_end else [])
    lab = "number line from %d to %d with jumps of %s" % (lo, hi, ", ".join(labs).replace("−", "minus "))
    return nl_svg(lo, hi, px_for(hi - lo), lab, extra=extra, dots=dots, arcs=arcs)


# ------------------------------------------------------------ bar drawings
def bars_svg(whole, parts, vals, subs, label):
    """Lengths end to end: bracket on top with the whole, one bar split into parts, words under the parts."""
    fs, sfs = 16, 14
    ws = []
    total = float(sum(vals))
    for t, v, sn in zip(parts, vals, subs):
        mn = max(tw(t, fs), tw(sn, sfs)) + 14
        ws.append(max(mn, 240 * v / total))
    bw = sum(ws)
    W = max(20 + bw, tw(whole, fs) + 20)
    x0 = (W - bw) / 2
    s = [text(x0 + bw / 2, 18, whole, col=RED if "?" in whole else INK)]
    s.append("<path d='M%.1f 34 v-8 H%.1f v8' fill='none' stroke='%s' stroke-width='2'/>" % (x0, x0 + bw, INK))
    x = x0
    for t, w, sn in zip(parts, ws, subs):
        unk = "?" in t
        s.append("<rect x='%.1f' y='40' width='%.1f' height='34' fill='%s' stroke='%s' stroke-width='2.5'%s/>"
                 % (x, w, PINK if unk else FILL, RED if unk else GREEN, " stroke-dasharray='5 3'" if unk else ""))
        s.append(text(x + w / 2, 63, t, col=RED if unk else INK))
        s.append(text(x + w / 2, 94, sn, fs=sfs))
        x += w
    return svg_wrap(int(W + 0.99), 102, "".join(s), label)


def cmp_svg(nb, ns, vb, vs, tb, ts, td, label):
    """Two bars: the longer one on top; the shorter bar plus a dashed part (the difference) underneath."""
    fs = 16
    lw = max(tw(nb, fs), tw(ns, fs))
    x0 = 10 + lw + 8
    L = 220.0
    dmin = max(48, tw(td, fs) + 16)
    ls = max(tw(ts, fs) + 16, 48, L * vs / vb)
    ls = min(ls, L - dmin)
    s = [text(x0 - 8, 27, nb, anchor="end"), text(x0 - 8, 69, ns, anchor="end")]
    s.append("<rect x='%.1f' y='6' width='%.1f' height='32' fill='%s' stroke='%s' stroke-width='2.5'/>" % (x0, L, FILL, GREEN))
    s.append(text(x0 + L / 2, 28, tb, col=RED if "?" in tb else INK))
    s.append("<rect x='%.1f' y='48' width='%.1f' height='32' fill='%s' stroke='%s' stroke-width='2.5'/>" % (x0, ls, FILL, GREEN))
    s.append(text(x0 + ls / 2, 70, ts, col=RED if "?" in ts else INK))
    s.append("<rect x='%.1f' y='48' width='%.1f' height='32' fill='%s' stroke='%s' stroke-width='2.5' stroke-dasharray='5 3'/>"
             % (x0 + ls, L - ls, PINK, RED))
    s.append(text(x0 + ls + (L - ls) / 2, 70, td, col=RED))
    return svg_wrap(int(x0 + L + 10.99), 86, "".join(s), label)


# ============================================================ set 1: numbers as lengths
def set_lengths(rnd, P):
    its = []
    # --- which number is at the dot? (big marks every 10 or every 5)
    dots = [(30, 10, 37), (60, 10, 74), (10, 10, 28), (40, 10, 46), (75, 5, 83), (20, 5, 32), (0, 5, 13)]
    for lo, step, v in dots:
        hi = lo + 20
        L = (v - lo) // step * step + lo
        Up = L + step
        o, back = v - L, Up - v
        assert 0 < o < step and lo <= v <= hi
        svg = nl_svg(lo, hi, 13, "number line from %d to %d with a dot" % (lo, hi), lab_every=step, dots=[(v, RED)])
        q = fig(svg) + "Each small space is 1. What number is at the red dot?"
        e = ("Find the big mark just before the dot: %d. Count the spaces after it, not the marks: %s. "
             "%d + %d = %d. (It is also %d before %d.)"
             % (L, ", ".join(str(L + k) for k in range(1, o + 1)), L, o, v, back, Up))
        wrong = [v - 1, Up + back, v + 10, v + 1]           # counted the first mark; counted from the wrong side; wrong ten
        its.append(mcq(q, v, wrong, e))
    # --- objects from 0: count spaces, not marks
    zero = [("crayon", "cm", 9), ("caterpillar", "cm", 5), ("leaf", "cm", 8), ("ribbon", "cm", 13),
            ("pencil", "in", 7), ("craft stick", "in", 6), ("paper strip", "in", 9)]
    for kind, u, n in zero:
        hi, px = (15, 24) if u == "cm" else (10, 30)
        svg = nl_svg(0, hi, px, "%s above a number line from 0 to %d in %s" % (kind, hi, UNITS[u][1]), lab_every=1, obj=(kind, 0, n))
        q = fig(svg) + "The number line is marked in %s. How long is the %s?" % (UNITS[u][1], kind)
        e = ("The %s starts at 0 and ends at %d. Count the spaces, not the marks: there are %d spaces. "
             "Each space is 1 %s, so it is %s long." % (kind, n, n, UNITS[u][0], U(n, u)))
        its.append(mcq(q, U(n, u), [U(n + 1, u), U(n, OTHER[u]), U(n - 1, u), U(n + 2, u)], e))
    # --- objects that do not start at 0
    mid = [("eraser", "cm", 4, 9), ("nail", "cm", 3, 10), ("paper strip", "cm", 5, 14), ("pencil", "cm", 2, 15),
           ("ribbon", "in", 3, 8), ("crayon", "in", 2, 6)]
    for kind, u, a, b in mid:
        hi, px = (15, 24) if u == "cm" else (10, 30)
        d = b - a
        svg = nl_svg(0, hi, px, "%s above a number line from 0 to %d in %s" % (kind, hi, UNITS[u][1]), lab_every=1, obj=(kind, a, b))
        q = fig(svg) + "The number line is marked in %s. How long is the %s?" % (UNITS[u][1], kind)
        e = ("The %s does not start at 0. It goes from %d to %d. Subtract: %d − %d = %d. "
             "Or count the spaces from %d to %d: %d. Answer: %s." % (kind, a, b, b, a, d, a, b, d, U(d, u)))
        its.append(mcq(q, U(d, u), [U(b, u), U(d + 1, u), U(a + b, u), U(d - 1, u)], e))
    assert len(its) == 20, len(its)
    return {"title": "Numbers as lengths on a number line", "items": its}


# ============================================================ set 2: jumps for adding and subtracting
def set_jumps(rnd, P):
    its = []
    # --- add: where do you land?
    for s0, j in [(45, 20), (23, 30), (58, 14), (36, 25), (17, 18), (64, 27)]:
        end = s0 + j
        svg = jump_svg(s0, [j])
        q = fig(svg) + "Start at %d. Jump %d to the right. Where do you land?" % (s0, j)
        e = "Moving right adds. Start at %d and move %d spaces: %d + %d = %s. %s" % (s0, j, s0, j, BOX, add_e(s0, j))
        its.append(mcq(q, end, [end - 1, end + 10, end - 10, s0 - j, end + 1], e))
    # --- subtract: jump to the left
    for s0, j in [(72, 30), (55, 16), (81, 25), (46, 19), (90, 37)]:
        end = s0 - j
        svg = jump_svg(s0, [-j])
        q = fig(svg) + "Start at %d. Jump %d to the left. Where do you land?" % (s0, j)
        e = "Moving left subtracts. Start at %d and move back %d spaces: %d − %d = %s. %s" % (s0, j, s0, j, BOX, sub_e(s0, j))
        w = [end + 1, s0 + j, end + 10, end - 10]
        if borrow(s0, j):
            w.insert(0, sub_err(s0, j))
        its.append(mcq(q, end, w, e))
    # --- how long is the jump?
    for a, b in [(34, 52), (48, 75), (26, 41), (57, 83)]:
        d = b - a
        svg = jump_svg(a, [d], end_text=str(b), label_jumps=["?"])
        q = fig(svg) + "How long is the jump from %d to %d?" % (a, b)
        e = ("Count up from %d to %d, or subtract: %d − %d = %d. Check: %d + %d = %d. "
             "Count the spaces, not the marks." % (a, b, b, a, d, a, d, b))
        w = [d + 1, sub_err(b, a) if borrow(b, a) else d + 10, a + b, d - 10, d - 1]
        its.append(mcq(q, d, w, e))
    # --- two jumps: which equation?
    for s0, jt, jo in [(30, 20, 5), (43, 20, 8)]:
        t = jt + jo
        svg = jump_svg(s0, [jt, jo])
        q = fig(svg) + "Which equation does the number line show?"
        e = ("The jumps are +%d and +%d. Together they make %d. Start at %d and add %d: %d + %d = %d."
             % (jt, jo, t, s0, t, s0, t, s0 + t))
        its.append(mcq(q, "%d + %d = %d" % (s0, t, s0 + t),
                       ["%d + %d = %d" % (s0, jt, s0 + jt), "%d + %d = %d" % (jt, jo, t), "%d + %d = %d" % (s0, jo, s0 + jo)], e))
    s0, jt, jo = 74, 20, 6
    t = jt + jo
    svg = jump_svg(s0, [-jt, -jo])
    its.append(mcq(fig(svg) + "Which equation does the number line show?", "%d − %d = %d" % (s0, t, s0 - t),
                   ["%d − %d = %d" % (s0, jt, s0 - jt), "%d + %d = %d" % (s0, t, s0 + t), "%d + %d = %d" % (jt, jo, t)],
                   "Both jumps go left, so subtract. −%d and −%d make −%d: %d − %d = %d." % (jt, jo, t, s0, t, s0 - t)))
    # --- which number line shows ... ? (A to D)
    for (s0, j, op), wrongs, why in [
        ((30, 25, "+"), [(30, -25), (30, 20), (0, 25)], "starts at 30 and jumps 25 to the right, to 55"),
        ((62, 24, "−"), [(62, 24), (62, -20), (62, -14)], "starts at 62 and jumps 24 to the left, to 38"),
    ]:
        right = (s0, j if op == "+" else -j)
        panels = [right] + wrongs
        order = [0, 1, 2, 3]
        rnd.shuffle(order)
        cells = [panels[i] for i in order]
        pos = order.index(0)
        svg = choice_lines_svg(cells)
        q = fig(svg) + "Which number line shows %d %s %d?" % (s0, op, j)
        e = "Number line %s %s. %d %s %d = %d." % ("ABCD"[pos], why, s0, op, j, s0 + right[1])
        its.append(mcq_fixed(q, "ABCD"[pos], e))
    assert len(its) == 20, len(its)
    return {"title": "Add and subtract with jumps", "items": its}


def choice_lines_svg(cells):
    """2 x 2 small number lines labeled A to D. Each cell: (start, jump)."""
    CW, CH = 196, 92
    s = ["<line x1='%d' y1='6' x2='%d' y2='%d' stroke='%s' stroke-width='1'/>" % (CW, CW, 2 * CH - 6, GREY),
         "<line x1='6' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='1'/>" % (CH, 2 * CW - 6, CH, GREY)]
    for k, (st, j) in enumerate(cells):
        x0, y0 = (k % 2) * CW, (k // 2) * CH
        ly = y0 + 58
        s.append(text(x0 + 8, y0 + 22, "ABCD"[k], 18, anchor="start"))
        xa, xb = (x0 + 52, x0 + 162) if j > 0 else (x0 + 162, x0 + 52)
        s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='2.2'/>" % (x0 + 32, ly, x0 + 182, ly, INK))
        for x in (xa, xb):
            s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='2'/>" % (x, ly - 7, x, ly + 7, INK))
        s.append("<path d='M %d %d C %d %d %d %d %d %d' fill='none' stroke='%s' stroke-width='2.5'/>"
                 % (xa, ly - 2, xa, ly - 34, xb, ly - 34, xb, ly - 2, GREEN))
        s.append("<polyline points='%d,%d %d,%d %d,%d' fill='none' stroke='%s' stroke-width='2.5' stroke-linejoin='round'/>"
                 % (xb - 5, ly - 11, xb, ly - 2, xb + 5, ly - 11, GREEN))
        s.append(text((xa + xb) / 2, ly - 31, ("+%d" % j) if j > 0 else ("−%d" % -j), 15, col=GREEN))
        s.append(text(xa, ly + 24, str(st), 15))
        s.append(text(xb, ly + 24, str(st + j), 15))
    return svg_wrap(2 * CW, 2 * CH, "".join(s), "four number lines labeled A to D")


# ============================================================ set 3: join lengths
# t: story ({a} {b} [{c}]), q: question, u: unit, lab: words under the bars, r: ranges for a and b
JOIN = [
    dict(t="{N} has a red ribbon {a} centimeters long and a blue ribbon {b} centimeters long. {He} tapes them end to end.",
         q="How long is the new ribbon?", u="cm", lab=("red", "blue"), r=((18, 45), (15, 40))),
    dict(t="{N} walks {a} meters to the corner. Then {he} walks {b} meters to the park.",
         q="How far does {he} walk in all?", u="m", lab=("to corner", "to park"), r=((20, 48), (25, 45))),
    dict(t="Dad puts two boards end to end. One board is {a} inches long. The other board is {b} inches long.",
         q="How long are the two boards together?", u="in", lab=("board 1", "board 2"), r=((24, 48), (26, 45))),
    dict(t="A garden fence has two parts. One part is {a} feet long. The other part is {b} feet long.",
         q="How long is the whole fence?", u="ft", lab=("part 1", "part 2"), r=((14, 40), (16, 38))),
    dict(t="{N} built a block tower {a} centimeters tall. Then {he} added blocks to make it {b} centimeters taller.",
         q="How tall is the tower now?", u="cm", lab=("at first", "added"), r=((25, 50), (12, 30))),
    dict(t="A sunflower was {a} inches tall. Then it grew {b} more inches.",
         q="How tall is the sunflower now?", u="in", lab=("at first", "grew"), r=((26, 50), (13, 28))),
    dict(t="{N} knit a scarf {a} inches long. Then {he} knit {b} more inches.",
         q="How long is the scarf now?", u="in", lab=("at first", "more"), r=((22, 40), (14, 30))),
    dict(t="A paper chain is {a} feet long. The class makes {b} more feet of chain.",
         q="How long is the chain now?", u="ft", lab=("at first", "more"), r=((18, 45), (12, 30))),
    dict(t="A worm crawled {a} centimeters. Then it crawled {b} centimeters more.",
         q="How far did the worm crawl in all?", u="cm", lab=("first", "then"), r=((12, 35), (11, 30))),
    dict(t="{N} swam {a} meters. Then {he} swam {b} more meters.",
         q="How far did {N} swim in all?", u="m", lab=("first", "then"), r=((25, 50), (15, 40))),
    dict(t="Two rugs lie end to end in a hallway. One rug is {a} feet long. The other rug is {b} feet long.",
         q="How long are the two rugs together?", u="ft", lab=("rug 1", "rug 2"), r=((7, 14), (6, 12))),
    dict(t="{N} lays a pencil and a crayon end to end. The pencil is {a} centimeters long. The crayon is {b} centimeters long.",
         q="How long are they together?", u="cm", lab=("pencil", "crayon"), r=((14, 19), (7, 9))),
    dict(t="A bean plant was {a} centimeters tall. It grew {b} centimeters this month.",
         q="How tall is the bean plant now?", u="cm", lab=("at first", "grew"), r=((15, 40), (12, 25))),
    dict(t="{N} rides {his} bike {a} meters to a friend's house. Then {he} rides {b} meters to school.",
         q="How far does {N} ride in all?", u="m", lab=("to friend", "to school"), r=((30, 55), (25, 44))),
    dict(t="Ms. Park hangs two banners end to end. One banner is {a} feet long. The other is {b} feet long.",
         q="How long are the two banners together?", u="ft", lab=("banner 1", "banner 2"), r=((8, 18), (7, 16))),
    dict(t="The class paints a red line {a} meters long on the playground. Then they paint a blue line {b} meters long at the end of it.",
         q="How long are the two lines together?", u="m", lab=("red", "blue"), r=((18, 45), (16, 40))),
    dict(t="A bookshelf is {a} inches long. {N} puts a second bookshelf {b} inches long next to it, end to end.",
         q="How long are the two shelves together?", u="in", lab=("shelf 1", "shelf 2"), r=((24, 40), (18, 36))),
]
THREE = [
    dict(t="A toy train has three cars. The cars are {a} centimeters, {b} centimeters and {c} centimeters long.",
         q="How long is the train?", u="cm", lab=("car 1", "car 2", "car 3")),
    dict(t="A trail has three parts. They are {a} meters, {b} meters and {c} meters long.",
         q="How long is the whole trail?", u="m", lab=("part 1", "part 2", "part 3")),
    dict(t="{N} tapes three paper strips end to end. They are {a} inches, {b} inches and {c} inches long.",
         q="How long is the long strip?", u="in", lab=("strip 1", "strip 2", "strip 3")),
]


def pick_pair(rnd, r, used, regroup, mx=99):
    while True:
        a, b = rnd.randint(*r[0]), rnd.randint(*r[1])
        if a != b and a + b <= mx and a % 10 and b % 10 and carry(a, b) == regroup and (a, b) not in used:
            used.add((a, b))
            return a, b


def set_join(rnd, P):
    its = []
    used = set()
    ctx = list(JOIN)
    rnd.shuffle(ctx)
    for i, c in enumerate(ctx):
        p = P.one()
        u = c["u"]
        a, b = pick_pair(rnd, c["r"], used, regroup=i % 4 != 0)
        tot = a + b
        story = say(c["t"], p, a=a, b=b)
        if i < 3:                                        # which equation?
            eq = "%d + %d = %s" % (a, b, BOX)
            big, sm = max(a, b), min(a, b)
            bad = ["%d − %d = %s" % (big, sm, BOX), "%d + %s = %d" % (a, BOX, b), "%d − %s = %d" % (b, BOX, a)]
            for x in bad:
                assert x.endswith(BOX) and eval(x.split(" = ")[0].replace("−", "-")) != tot or not x.endswith(BOX) and not solve_box(x, tot), x
            q = story + " Which equation matches the story?"
            e = "The two lengths are put together, so add: %s. %d + %d = %d, so the total is %s." % (eq, a, b, tot, U(tot, u))
            its.append(mcq(q, eq, bad, e))
            continue
        q = story + " " + say(c["q"], p)
        e = "The lengths are put together, so add: %d + %d = %s. %s Answer: %s." % (a, b, BOX, add_e(a, b), U(tot, u))
        if carry(a, b):
            e = e.replace(" Answer", " (%d + %d ones make a new ten.) Answer" % (a % 10, b % 10))
        if i % 2 == 1:
            q = fig(bars_svg("? %s" % UNITS[u][2], [S(a, u), S(b, u)], [a, b], list(c["lab"]),
                             "bar drawing of two lengths put together")) + q
        its.append(mcq(q, U(tot, u), [U(v, u) for v in add_wrong(a, b)], e))
    for c in THREE:
        p = P.one()
        u = c["u"]
        while True:
            lo, hi = {"cm": (12, 19), "m": (15, 35), "in": (9, 24)}[u]
            a, b, d = rnd.randint(lo, hi), rnd.randint(lo, hi), rnd.randint(lo, hi)
            if len({a, b, d}) == 3 and a + b + d <= 95 and (a % 10 + b % 10 + d % 10) >= 10 and a % 10 and b % 10 and d % 10:
                break
        tot = a + b + d
        q = fig(bars_svg("? %s" % UNITS[u][2], [S(a, u), S(b, u), S(d, u)], [a, b, d], list(c["lab"]),
                         "bar drawing of three lengths put together")) + say(c["t"] + " " + c["q"], p, a=a, b=b, c=d)
        e = ("Add all three lengths: %d + %d + %d = %s. First %d + %d = %d. Then %d + %d = %d. Answer: %s."
             % (a, b, d, BOX, a, b, a + b, a + b, d, tot, U(tot, u)))
        its.append(mcq(q, U(tot, u), [U(v, u) for v in [a + b, tot - 10, tot + 10, tot - 1, b + d]], e))
    assert len(its) == 20, len(its)
    return {"title": "Join lengths: put them end to end", "items": its}


# ============================================================ set 4: take away and compare
TAKE = [
    dict(t="A rope is {a} centimeters long. {N} cuts off {b} centimeters.", q="How long is the rope now?", u="cm",
         lab=("cut off", "left"), r=((50, 90), (15, 38))),
    dict(t="A ribbon is {a} inches long. {N} cuts off {b} inches to make a bow.", q="How much ribbon is left?", u="in",
         lab=("bow", "left"), r=((40, 72), (12, 26))),
    dict(t="A board is {a} inches long. Dad saws off {b} inches.", q="How long is the board now?", u="in",
         lab=("sawed off", "left"), r=((48, 96), (15, 40))),
    dict(t="A roll of tape had {a} feet of tape. The class used {b} feet.", q="How many feet of tape are left?", u="ft",
         lab=("used", "left"), r=((40, 75), (12, 35))),
    dict(t="A race is {a} meters long. {N} has run {b} meters.", q="How many more meters does {he} need to run?", u="m",
         lab=("ran", "still to run"), r=((60, 100), (21, 48)),
         lead="You know the whole race and the part already run. Subtract to find the part still to run:"),
    dict(t="A string is {a} centimeters long. {N} uses {b} centimeters to make a necklace.", q="How much string is left?", u="cm",
         lab=("necklace", "left"), r=((50, 90), (25, 45))),
    dict(t="A candle was {a} centimeters tall. It burned down {b} centimeters.", q="How tall is the candle now?", u="cm",
         lab=("burned", "left"), r=((24, 35), (7, 16))),
    dict(t="A garden hose is {a} feet long. A piece {b} feet long is cut off.", q="How long is the hose now?", u="ft",
         lab=("cut off", "left"), r=((50, 75), (13, 28))),
    dict(t="{N} has to walk {a} meters to the library. {He} has walked {b} meters so far.", q="How much farther does {he} have to walk?", u="m",
         lab=("walked", "to go"), r=((70, 98), (25, 55)),
         lead="You know the whole way and the part already walked. Subtract to find the part still to go:"),
    dict(t="A roll of paper is {a} feet long. {N} cuts off {b} feet for a class poster.", q="How long is the roll now?", u="ft",
         lab=("poster", "left"), r=((30, 60), (8, 19))),
]
# kinds: D = how much longer/taller, S = smaller unknown, B = bigger unknown
# n1/n2: names of the long and the short thing for the picture
CMP = [
    dict(k="D", t="A tree is {big} feet tall. A fence is {small} feet tall.", q="How much taller is the tree than the fence?", u="ft",
         n=("tree", "fence"), r=(24, 45, 5, 8)),
    dict(k="D", t="{A} is {big} inches tall. {B} is {small} inches tall.", q="How much taller is {A} than {B}?", u="in",
         n=("{A}", "{B}"), r=(48, 54, 41, 47)),
    dict(k="D", t="A green toy snake is {big} centimeters long. A red toy snake is {small} centimeters long.",
         q="How much longer is the green snake?", u="cm", n=("green", "red"), r=(52, 90, 21, 48)),
    dict(k="D", t="{A} jumped {big} inches. {B} jumped {small} inches.", q="How much farther did {A} jump than {B}?", u="in",
         n=("{A}", "{B}"), r=(44, 68, 25, 42)),
    dict(k="D", t="The big pool is {big} meters long. The small pool is {small} meters long.", q="How much shorter is the small pool?", u="m",
         n=("big pool", "small pool"), r=(25, 25, 8, 12)),
    dict(k="D", t="A sunflower is {big} inches tall. A tulip is {small} inches tall.", q="How much shorter is the tulip than the sunflower?", u="in",
         n=("sunflower", "tulip"), r=(62, 84, 14, 22)),
    dict(k="S", t="A blue ribbon is {big} centimeters long. A red ribbon is {d} centimeters shorter than the blue ribbon.",
         q="How long is the red ribbon?", u="cm", n=("blue", "red"), r=(45, 80, 12, 29),
         lead="The red ribbon is shorter, so subtract:"),
    dict(k="S", t="A school bus is {big} feet long. It is {d} feet longer than a van.", q="How long is the van?", u="ft",
         n=("bus", "van"), r=(38, 42, 21, 26),
         lead="The word “longer” is in the story, but the van is the shorter one, so subtract:"),
    dict(k="B", t="{A}'s paper airplane flew {small} feet. {B}'s plane flew {d} feet farther.", q="How far did {B}'s plane fly?", u="ft",
         n=("{B}", "{A}"), r=(13, 26, 8, 17),
         lead="{B}'s plane flew farther, so add:"),
    dict(k="B", t="A desk is {small} inches tall. It is {d} inches shorter than a bookshelf.", q="How tall is the bookshelf?", u="in",
         n=("shelf", "desk"), r=(27, 30, 25, 46),
         lead="The word “shorter” is in the story, but the bookshelf is the taller one, so add:"),
]


def set_take_compare(rnd, P):
    its = []
    used = set()
    take = list(TAKE)
    rnd.shuffle(take)
    for i, c in enumerate(take):
        p = P.one()
        u = c["u"]
        while True:
            a, b = rnd.randint(*c["r"][0]), rnd.randint(*c["r"][1])
            if b % 10 and (a - b) % 10 and borrow(a, b) == (i % 4 != 0) and a != 2 * b and (a, b) not in used:
                break
        used.add((a, b))
        d = a - b
        q = say(c["t"] + " " + c["q"], p, a=a, b=b)
        lead = c.get("lead", "Part of the length is taken away, so subtract:")
        e = "%s %d − %d = %s. %s Check: %d + %d = %d. Answer: %s." % (
            lead, a, b, BOX, sub_e(a, b), d, b, a, U(d, u))
        if i % 2 == 0:
            q = fig(bars_svg(S(a, u), [S(b, u), "? %s" % UNITS[u][2]], [b, d], list(c["lab"]),
                             "bar drawing of a length with a part taken away")) + q
        its.append(mcq(q, U(d, u), [U(v, u) for v in sub_wrong(a, b)], e))
    cmps = list(CMP)
    rnd.shuffle(cmps)
    for c in cmps:
        p = P.two()
        u = c["u"]
        r = c["r"]
        while True:
            if c["k"] == "D":
                big, small = rnd.randint(r[0], r[1]), rnd.randint(r[2], r[3])
                d = big - small
            elif c["k"] == "S":
                big, d = rnd.randint(r[0], r[1]), rnd.randint(r[2], r[3])
                small = big - d
            else:
                small, d = rnd.randint(r[0], r[1]), rnd.randint(r[2], r[3])
                big = small + d
            if big <= 100 and small >= 3 and d >= 3 and d != small and (big - small) % 10 and small % 10 and big % 10:
                break
        story = say(c["t"], p, big=big, small=small, d=d)
        q = story + " " + say(c["q"], p)
        n1, n2 = say(c["n"][0], p), say(c["n"][1], p)
        if c["k"] == "D":
            ans = d
            e = ("To compare, find the difference. Subtract the shorter length from the longer one: %d − %d = %s. %s "
                 "Check: %d + %d = %d. Answer: %s." % (big, small, BOX, sub_e(big, small), small, d, big, U(d, u)))
            if "shorter" in c["q"]:
                e += " “How much shorter” is the same difference."
            w = sub_wrong(big, small)
        elif c["k"] == "S":
            ans = small
            e = "%s %d − %d = %s. %s Answer: %s." % (say(c["lead"], p), big, d, BOX, sub_e(big, d), U(small, u))
            w = [big + d] + ([sub_err(big, d)] if borrow(big, d) else []) + [small + 10, small - 10, small + 1]
            q = fig(cmp_svg(n1, n2, big, small, S(big, u), "?", S(d, u), "comparison bars for two lengths")) + q
        else:
            ans = big
            e = "%s %d + %d = %s. %s Answer: %s." % (say(c["lead"], p), small, d, BOX, add_e(small, d), U(big, u))
            w = [abs(small - d)] + add_wrong(small, d)[:-2] + [big + 1]
            q = fig(cmp_svg(n1, n2, big, small, "?", S(small, u), S(d, u), "comparison bars for two lengths")) + q
        its.append(mcq(q, U(ans, u), [U(v, u) for v in w], e))
    assert len(its) == 20, len(its)
    return {"title": "Take away and compare lengths", "items": its}


# ============================================================ set 5: missing lengths and two-step stories
def set_unknown(rnd, P):
    its = []
    # start unknown, take from: ☐ − b = c
    p = P.one()
    a, b = 64, 18
    c = a - b
    its.append(mcq(fig(bars_svg("? in.", [S(c, "in"), S(b, "in")], [c, b], ["left", "cut off"], "bar drawing with the start unknown"))
                   + say("A ribbon was some inches long. {N} cut off {b} inches. Now the ribbon is {c} inches long. How long was it at first?", p, b=b, c=c),
                   U(a, "in"), [U(v, "in") for v in [c - b, a - 10, a + 10, a - 1]],
                   "The start is unknown: %s − %d = %d. Put the cut piece back: %d + %d = %d. Answer: %s." % (BOX, b, c, c, b, a, U(a, "in"))))
    # start unknown, add to: ☐ + b = c
    p = P.one()
    a, b = 37, 16
    c = a + b
    its.append(mcq(fig(bars_svg(S(c, "cm"), ["? cm", S(b, "cm")], [a, b], ["at first", "grew"], "bar drawing with the start unknown"))
                   + "A plant grew %d centimeters this month. Now it is %d centimeters tall. How tall was it at the start of the month?" % (b, c),
                   U(a, "cm"), [U(v, "cm") for v in [c + b, sub_err(c, b), a + 10, a + 1]],
                   "The start is unknown: %s + %d = %d. Take away what it grew: %d − %d = %d. Answer: %s." % (BOX, b, c, c, b, a, U(a, "cm"))))
    # change unknown, add to, on a number line: a + ☐ = c
    for a, c, u, t in [(28, 45, "cm", "A bean plant was {a} centimeters tall. It grew some more. Now it is {c} centimeters tall. How many centimeters did it grow?"),
                       (36, 62, "ft", "A paper chain was {a} feet long. The class made it longer. Now it is {c} feet long. How many feet did they add?")]:
        d = c - a
        q = fig(jump_svg(a, [d], end_text=str(c), label_jumps=["+?"])) + t.format(a=a, c=c)
        e = ("The change is unknown: %d + %s = %d. Count up from %d to %d on the number line, or subtract: %d − %d = %d. Answer: %s."
             % (a, BOX, c, a, c, c, a, d, U(d, u)))
        its.append(mcq(q, U(d, u), [U(v, u) for v in [a + c, d + 1, sub_err(c, a), d + 10, d - 10]], e))
    # change unknown, take from, words only: a − ☐ = c
    for a, c, u, t in [(80, 53, "cm", "A rope was {a} centimeters long. {N} cut some off. Now it is {c} centimeters long. How much did {he} cut off?"),
                       (95, 68, "m", "{N} has to walk {a} meters to the park. {He} has {c} meters left to go. How far has {he} walked so far?")]:
        p = P.one()
        d = a - c
        q = say(t, p, a=a, c=c)
        e = ("The change is unknown: %d − %s = %d. Think: %d + %s = %d. Subtract: %d − %d = %d. Answer: %s."
             % (a, BOX, c, c, BOX, a, a, c, d, U(d, u)))
        its.append(mcq(q, U(d, u), [U(v, u) for v in [a + c, sub_err(a, c), d + 10, d - 1]], e))
    # which equation?
    eqs = [
        ("A rope was some feet long. {N} cut off {b} feet. Now it is {c} feet long.", 19, 46, "%s − %d = %d", "start"),
        ("A tower was {a} centimeters tall. {N} added some blocks. Now it is {c} centimeters tall.", 34, 61, "%d + %s = %d", "change"),
        ("A ribbon was {a} inches long. {N} cut off some. Now it is {c} inches long.", 72, 45, "%d − %s = %d", "change-"),
        ("A sunflower grew {b} inches. Now it is {c} inches tall.", 17, 58, "%s + %d = %d", "start+"),
    ]
    for t, x, y, form, kind in eqs:
        p = P.one()
        if kind == "start":
            b, c = x, y
            eq, ans = form % (BOX, b, c), b + c
            q = say(t, p, b=b, c=c) + " Which equation can you use to find how long it was at first?"
            bad = ["%d − %d = %s" % (c, b, BOX), "%s + %d = %d" % (BOX, b, c), "%d − %s = %d" % (c, BOX, b)]
            why = "The start is unknown, and %d feet were cut off: %s. Answer: %d + %d = %d feet." % (b, eq, c, b, ans)
        elif kind == "change":
            a, c = x, y
            eq, ans = form % (a, BOX, c), c - a
            q = say(t, p, a=a, c=c) + " Which equation can you use to find how much taller it got?"
            bad = ["%d + %d = %s" % (a, c, BOX), "%d − %s = %d" % (a, BOX, c), "%s − %d = %d" % (BOX, a, c)]
            why = "The tower got taller by an unknown amount: %s. Answer: %d − %d = %d centimeters." % (eq, c, a, ans)
        elif kind == "change-":
            a, c = x, y
            eq, ans = form % (a, BOX, c), a - c
            q = say(t, p, a=a, c=c) + " Which equation can you use to find how much was cut off?"
            bad = ["%d + %d = %s" % (a, c, BOX), "%d + %s = %d" % (a, BOX, c), "%s − %d = %d" % (BOX, a, c)]
            why = "An unknown length was cut off: %s. Answer: %d − %d = %d inches." % (eq, a, c, ans)
        else:
            b, c = x, y
            eq, ans = form % (BOX, b, c), c - b
            q = say(t, p, b=b, c=c) + " Which equation can you use to find how tall it was before?"
            bad = ["%d + %d = %s" % (b, c, BOX), "%s − %d = %d" % (BOX, b, c), "%d − %s = %d" % (b, BOX, c)]
            why = "The start is unknown, and it grew %d inches: %s. Answer: %d − %d = %d inches." % (b, eq, c, b, ans)
        assert solve_box(eq, ans), (eq, ans)
        for z in bad:
            if z.endswith(BOX):
                assert eval(z.split(" = ")[0].replace("−", "-")) != ans, z
            else:
                assert not solve_box(z, ans), z
        its.append(mcq(q, eq, bad, why))
    # two-step stories
    two = []

    def T(q, s1, s2, eq, ans, u, wrong):
        two.append((q, s1, s2, eq, ans, u, wrong))

    p = P.one()
    a, b, c = 90, 25, 32
    T(say("A board is {a} inches long. {N} saws off {b} inches. Then {he} saws off {c} more inches. How long is the board now?", p, a=a, b=b, c=c),
      "First cut: %d − %d = %d." % (a, b, a - b), "Second cut: %d − %d = %d." % (a - b, c, a - b - c),
      "%d − %d − %d = %s" % (a, b, c, BOX), a - b - c, "in", [a - b, b + c, a - b + c, a - b - c + 10])
    q2 = P.two()
    a, d = 36, 15
    T("%s's block tower is %d centimeters tall. %s's tower is %d centimeters taller. %s puts %s tower on top of %s's tower. How tall is the new tower?"
      % (q2["A"], a, q2["B"], d, q2["B"], "her" if q2["heB"] == "she" else "his", q2["A"]),
      "%s's tower: %d + %d = %d." % (q2["B"], a, d, a + d), "Together: %d + %d = %d." % (a, a + d, 2 * a + d),
      "%d + %d + %d = %s" % (a, a, d, BOX), 2 * a + d, "cm", [a + d, 2 * a, 2 * a + d - 10, 2 * a - d])
    a, b, c = 80, 26, 35
    T("A path is %d meters long. The class walked %d meters. Then they walked %d more meters. How much farther is it to the end of the path?" % (a, b, c),
      "Walked: %d + %d = %d." % (b, c, b + c), "Still to go: %d − %d = %d." % (a, b + c, a - b - c),
      "%d − %d − %d = %s" % (a, b, c, BOX), a - b - c, "m", [b + c, a - b, a - c, a - b - c + 10])
    p = P.one()
    a, d = 34, 18
    T(say("{N} has a red ribbon {a} centimeters long. {His} blue ribbon is {d} centimeters longer. {He} tapes them end to end. How long is the new ribbon?", p, a=a, d=d),
      "Blue ribbon: %d + %d = %d." % (a, d, a + d), "Both: %d + %d = %d." % (a, a + d, 2 * a + d),
      "%d + %d + %d = %s" % (a, a, d, BOX), 2 * a + d, "cm", [a + d, 2 * a + d - 10, 2 * a, a + d + d])
    a, b, c = 60, 23, 19
    T("A fence will be %d feet long. Workers built %d feet on Monday and %d feet on Tuesday. How many more feet do they need to build?" % (a, b, c),
      "Built: %d + %d = %d." % (b, c, b + c), "Still to build: %d − %d = %d." % (a, b + c, a - b - c),
      "%d − %d − %d = %s" % (a, b, c, BOX), a - b - c, "ft", [b + c, a - b, a - c, a - b - c + 10])
    a, b, c = 25, 12, 16
    T("A sunflower was %d inches tall. It grew %d inches in June and %d inches in July. How tall is it now?" % (a, b, c),
      "June: %d + %d = %d." % (a, b, a + b), "July: %d + %d = %d." % (a + b, c, a + b + c),
      "%d + %d + %d = %s" % (a, b, c, BOX), a + b + c, "in", [a + b, a + c, a + b + c - 10, a + b + c + 10])
    p = P.one()
    a, b, c = 75, 24, 18
    T(say("A rope is {a} centimeters long. {N} cuts off a piece {b} centimeters long and a piece {c} centimeters long. How much rope is left?", p, a=a, b=b, c=c),
      "Cut off: %d + %d = %d." % (b, c, b + c), "Left: %d − %d = %d." % (a, b + c, a - b - c),
      "%d − %d − %d = %s" % (a, b, c, BOX), a - b - c, "cm", [b + c, a - b, a - b - c + 10, a - b + c])
    p = P.one()
    a, b, c = 47, 15, 84
    T(say("{N} is {a} inches tall. {He} stands on a box that is {b} inches tall. A door is {c} inches tall. How much taller is the door than {N} on the box?", p, a=a, b=b, c=c),
      "%s on the box: %d + %d = %d." % (p["N"], a, b, a + b), "Difference: %d − %d = %d." % (c, a + b, c - a - b),
      "%d − %d − %d = %s" % (c, a, b, BOX), c - a - b, "in", [c - a, a + b, c - a - b + 10, c - b])
    a, b, c = 100, 45, 28
    p = P.one()
    T(say("A race is {a} meters long. {N} ran {b} meters. Then {he} walked {c} meters. How much farther does {he} have to go?", p, a=a, b=b, c=c),
      "So far: %d + %d = %d." % (b, c, b + c), "Still to go: %d − %d = %d." % (a, b + c, a - b - c),
      "%d − %d − %d = %s" % (a, b, c, BOX), a - b - c, "m", [b + c, a - b, a - b - c + 10, a - c])
    q3 = P.two()
    n3 = P.next()
    while n3[0] in (q3["A"], q3["B"]):
        n3 = P.next()
    a, d, f = 38, 9, 6
    T("%s jumped %d inches. %s jumped %d inches farther than %s. %s's jump was %d inches shorter than %s's. How far did %s jump?"
      % (q3["A"], a, q3["B"], d, q3["A"], n3[0], f, q3["B"], n3[0]),
      "%s: %d + %d = %d." % (q3["B"], a, d, a + d), "%s: %d − %d = %d." % (n3[0], a + d, f, a + d - f),
      "%d + %d − %d = %s" % (a, d, f, BOX), a + d - f, "in", [a + d, a + d + f, a - f, a - d + f])
    for q, s1, s2, eq, ans, u, wrong in two:
        nums = [int(x) for x in re.findall(r"\d+", eq)]
        assert all(1 <= v <= 100 for v in nums + [ans]) and ans not in nums, (eq, ans)
        e = "Step 1: %s Step 2: %s Equation: %s. Answer: %s." % (s1, s2, eq, U(ans, u))
        its.append(mcq(q, U(ans, u), [U(v, u) for v in wrong + [ans + 1, ans - 1]], e))
    assert len(its) == 20, len(its)
    return {"title": "Missing lengths and two-step stories", "items": its}


# ============================================================ lesson
def ex(title, q, s, a):
    return ("<div class='sn-ex'><span class='sn-ex-t'>%s</span><p class='sn-ex-q'>%s</p>"
            "<p class='sn-ex-s'>%s</p><p class='sn-ex-a'>Answer: %s</p></div>" % (title, q, s, a))


def table(head, rows):
    h = "".join("<th>%s</th>" % x for x in head)
    b = "".join("<tr>" + "".join("<td>%s</td>" % c for c in r) + "</tr>" for r in rows)
    return "<div class='sn-tw'><table class='sn-table'><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>" % (h, b)


def body_html():
    return (
        "<h2>A number is a length from 0</h2>"
        "<p>On a number line, the marks are <b>equally spaced</b>. Each space is 1 unit, like 1 centimeter or 1 inch. "
        "The number 7 is <b>7 spaces from 0</b>. So a length is the number of spaces, not the number of marks.</p>"
        "<figure class='sn-fig'>" +
        nl_svg(0, 10, 30, "crayon above a number line from 0 to 10 in centimeters", lab_every=1, obj=("crayon", 0, 7)) +
        "<figcaption>The crayon goes from 0 to 7. There are 7 spaces, so it is 7 centimeters long. "
        "There are 8 marks, but the length is 7.</figcaption></figure>"
        "<h2>Add and subtract with jumps</h2>"
        "<p>To add, start at the first number and <b>jump right</b>. To subtract, <b>jump left</b>. "
        "Big jumps of 10 first, then small jumps, make it easy.</p>"
        "<figure class='sn-fig'>" + jump_svg(45, [20], end_text="65") +
        "<figcaption>Start at 45. Jump 20 to the right. You land on 65: 45 + 20 = 65.</figcaption></figure>"
        "<figure class='sn-fig'>" + jump_svg(62, [-20, -4], end_text="38") +
        "<figcaption>62 − 24: jump back 20 to 42, then back 4 to 38. So 62 − 24 = 38.</figcaption></figure>"
        "<h2>Draw the story, then write an equation</h2>"
        "<p>Draw the lengths as bars. Put a <b>☐</b> where the unknown number goes. "
        "All the lengths in one story use the <b>same unit</b>.</p>"
        "<figure class='sn-fig'>" +
        bars_svg("60 cm", ["25 cm", "? cm"], [25, 35], ["cut off", "left"], "bar drawing of a rope with a piece cut off") +
        "<figcaption>A rope is 60 cm long. 25 cm is cut off. The two parts make the whole rope.</figcaption></figure>" +
        ex("Take away", "A rope is 60 centimeters long. Ava cuts off 25 centimeters. How long is the rope now?",
           "Part is taken away, so subtract: 60 − 25 = ☐. 60 − 20 = 40, then 40 − 5 = 35.", "35 centimeters") +
        ex("Compare", "A tree is 32 feet tall. A fence is 6 feet tall. How much taller is the tree than the fence?",
           "Find the difference: 32 − 6 = ☐. Count up from 6 to 32: that is 26.", "26 feet") +
        ex("Missing start", "A ribbon was some inches long. Leo cut off 18 inches. Now it is 46 inches long. How long was it at first?",
           "☐ − 18 = 46. Put the cut piece back: 46 + 18 = 64.", "64 inches") +
        "<h2>Common mistakes</h2>" +
        table(["Mistake", "What to do instead"], [
            ["Counting the marks: the crayon is 8 cm", "Count the spaces between the marks: 7 cm"],
            ["Reading the end of a length that does not start at 0", "Subtract the start from the end: 9 − 4 = 5"],
            ["Counting the start number as the first jump", "Start at 45, then count 46, 47, … The first step lands on 46."],
            ["Adding when the question asks “how much longer”", "Compare means find the difference: subtract"],
            ["Writing the wrong unit", "Use the unit in the story: feet stay feet"],
        ])
    )


FAQ = [
    {"q": "What are length word problems in 2nd grade?",
     "a": "They are add and subtract stories about lengths, like ribbons, ropes, plants and paths, with numbers up to 100. All the lengths in one problem use the same unit, such as centimeters or feet."},
    {"q": "Why do 2nd graders use a number line for length?",
     "a": "A number line works like a ruler: each number is a length from 0. Children see adding as a jump to the right and subtracting as a jump to the left."},
    {"q": "Why do children get the wrong length on a number line or ruler?",
     "a": "They count the marks instead of the spaces, so they get 1 too many. A length is the number of spaces from the start to the end."},
    {"q": "Do 2nd graders convert units in word problems?",
     "a": "No. In 2nd grade every length in a problem uses the same unit. Converting units, like feet to inches, comes in 4th grade."},
]


def gen():
    rnd = random.Random(213)
    P = People(rnd)
    sets = [set_lengths(rnd, P), set_jumps(rnd, P), set_join(rnd, P), set_take_compare(rnd, P), set_unknown(rnd, P)]
    balance(sets, rnd)
    seen = set()
    for s in sets:
        assert len(s["items"]) == 20, (s["title"], len(s["items"]))
        assert sorted(it["a"] for it in s["items"]) == sorted([0, 1, 2, 3] * 5), s["title"]
        for it in s["items"]:
            assert len(set(it["c"])) == 4, it
            for c in it["c"]:
                for n in re.findall(r"\d+", c):
                    assert 0 < int(n) <= 100, c
            assert it["q"] not in seen, it["q"]
            seen.add(it["q"])
    u = {
        "country": "us", "subject": "math", "grade": "grade-2", "slug": "length-word-problems", "sort": 13,
        "updated": UPDATED, "pdf_url": "",
        "title": "Length Word Problems and Number Lines",
        "seo_title": "Grade 2 Length Word Problems Worksheets: Number Lines, Adding and Subtracting Lengths within 100",
        "short_title": "Length word problems",
        "domain": "Measurement and Data",
        "standard_code": "2.MD.B.5–6",
        "standard_url": "https://www.thecorestandards.org/Math/Content/2/MD/B/",
        "standard_text": "Use addition and subtraction within 100 to solve word problems involving lengths that are given in the same units, e.g., by using drawings (such as drawings of rulers) and equations with a symbol for the unknown number to represent the problem. Represent whole numbers as lengths from 0 on a number line diagram with equally spaced points corresponding to the numbers 0, 1, 2, …, and represent whole-number sums and differences within 100 on a number line diagram.",
        "meta_desc": "Free Grade 2 length word problem worksheets: numbers as lengths on a number line, adding and subtracting with jumps, joining, cutting and comparing lengths, missing lengths with ☐ equations and two-step stories. 100 practice questions with simple answers.",
        "key_big": "A length is the number of spaces from the start to the end.",
        "key_sub": "On a number line, jump right to add and left to subtract. In a story, draw the lengths, write an equation with a ☐ and keep the same unit: 60 cm − 25 cm = 35 cm.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }
    return mark_large(u, "(number line|labeled A to D)")


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
