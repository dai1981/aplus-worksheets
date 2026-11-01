# -*- coding: utf-8 -*-
"""
US Grade 4 Math: Number and Shape Patterns (4.OA.C.5)
  python tools/gen_us_math_g4_patterns.py
HTML attributes use single quotes (no backslashes in the JSON).
Grade 4 style: numbers 1,000 and above are written with commas.
"""
import json, os, random, re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "us", "math", "grade-4")
UPDATED = "2026-11-02"
GREEN = "#006633"
FILL = "#cfe6d6"
FILL2 = "#eef6f0"
RED = "#c0392b"
INK = "#2b2b2b"
WOOD = "#a0692a"
FONT = "Arial, Helvetica, sans-serif"
GIRLS = ["Maya", "Ava", "Mia", "Zoe", "Lily", "Emma", "Nora", "Ruby", "Sofia", "Grace"]
BOYS = ["Leo", "Noah", "Eli", "Sam", "Ben", "Omar", "Kai", "Jack", "Luis", "Owen"]


# ------------------------------------------------------------ helpers
def f(n):
    """Grade 4 style: 4536 -> 4,536."""
    return "{:,}".format(n)


def mcq(q, correct, cands, e, rnd):
    """4 choices: correct + 3 unique distractors (no zero or negative numbers)."""
    correct = str(correct)
    seen = {correct}
    pick = []
    for c in cands:
        c = str(c)
        lead = c.split(" ")[0].lstrip("$")
        if c in seen or not c or lead.startswith("-") or lead == "0":
            continue
        seen.add(c)
        pick.append(c)
        if len(pick) == 3:
            break
    assert len(pick) == 3, (q, correct, cands)
    ch = pick + [correct]
    rnd.shuffle(ch)
    return {"q": q, "c": ch, "a": ch.index(correct), "e": e}


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


def pl(n, w):
    return "%s %s" % (f(n), w if n == 1 else w + "s")


def ordn(n):
    if 10 <= n % 100 <= 20:
        suf = "th"
    else:
        suf = {1: "st", 2: "nd", 3: "rd"}.get(n % 10, "th")
    return "%d%s" % (n, suf)


def fig(svg):
    return "<div class='qfig'>" + svg + "</div>"


def svg_wrap(w, h, body, label):
    return ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 %d %d' width='%d' height='%d' "
            "role='img' aria-label='%s'><g font-family='%s'>%s</g></svg>" % (w, h, w, h, label, FONT, body))


def text(x, y, t, fs=16, anchor="middle", bold=True, col=INK):
    return ("<text x='%.1f' y='%.1f' font-size='%d'%s fill='%s' text-anchor='%s'>%s</text>"
            % (x, y, fs, " font-weight='700'" if bold else "", col, anchor, t))


# ------------------------------------------------------------ number patterns
def rule_txt(op, k):
    return {"add": "Add %s", "sub": "Subtract %s", "mul": "Multiply by %s"}[op] % f(k)


def step(x, op, k):
    return {"add": x + k, "sub": x - k, "mul": x * k}[op]


def seq(s, op, k, n):
    out = [s]
    while len(out) < n:
        out.append(step(out[-1], op, k))
    return out


def lst(xs):
    return ", ".join(f(x) for x in xs)


def sign(op):
    return {"add": "+", "sub": "−", "mul": "×"}[op]


def jumps(xs, op, k):
    return ", ".join("%s %s %s = %s" % (f(a), sign(op), f(k), f(b)) for a, b in zip(xs, xs[1:]))


def show(xs, tail="?"):
    return "<b>" + lst(xs) + (", " + tail if tail else "") + "</b>"


# ------------------------------------------------------------ shape patterns (figures)
S = 16          # one square / dot cell


def sq(x, y, s=S, fill=FILL):
    return ("<rect x='%.1f' y='%.1f' width='%d' height='%d' fill='%s' stroke='%s' stroke-width='2'/>"
            % (x, y, s, s, fill, GREEN))


def shp_grid(n, p):
    """p = (rows, extra columns, 'sq' or 'dot'): figure n has (n + extra) columns of `rows` squares or dots."""
    h, c, kind = p
    cols = n + c
    s = []
    for i in range(cols):
        for j in range(h):
            x, y = i * S, j * S
            if kind == "sq":
                s.append(sq(x, y))
            else:
                s.append("<circle cx='%.1f' cy='%.1f' r='5.5' fill='%s'/>" % (x + S / 2, y + S / 2, GREEN))
    return cols * S, h * S, s, h * cols


def shp_L(n, p):
    """L shape: one corner square, an arm of n + p squares going up and n + p going right."""
    a = n + p
    s = []
    for j in range(a + 1):
        s.append(sq(0, j * S))
    for i in range(1, a + 1):
        s.append(sq(i * S, a * S))
    return (a + 1) * S, (a + 1) * S, s, 2 * a + 1


def shp_cross(n, p):
    """Plus sign: a middle square with 4 arms of n + p squares."""
    a = n + p
    C = 14
    s = []
    for i in range(2 * a + 1):
        s.append(sq(i * C, a * C, C, FILL))
        if i != a:
            s.append(sq(a * C, i * C, C, FILL))
    s.append(sq(a * C, a * C, C, FILL2))
    return (2 * a + 1) * C, (2 * a + 1) * C, s, 4 * a + 1


def stick(x1, y1, x2, y2):
    """One toothpick, a little shorter than the side so every stick can be seen and counted."""
    dx, dy = x2 - x1, y2 - y1
    t = 4.0 / max(abs(dx), abs(dy), 1) if dx == 0 or dy == 0 else 4.0 / ((dx * dx + dy * dy) ** 0.5)
    return ("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='4' stroke-linecap='round'/>"
            % (x1 + dx * t, y1 + dy * t, x2 - dx * t, y2 - dy * t, WOOD))


L_ST = 28


def shp_sticks_sq(n, p):
    """Row of n + p squares made of toothpicks: 3 × squares + 1 sticks."""
    m = n + p
    s = []
    for i in range(m):
        s.append(stick(i * L_ST, 2, (i + 1) * L_ST, 2))
        s.append(stick(i * L_ST, L_ST + 2, (i + 1) * L_ST, L_ST + 2))
    for i in range(m + 1):
        s.append(stick(i * L_ST, 2, i * L_ST, L_ST + 2))
    return m * L_ST + 2, L_ST + 4, s, 3 * m + 1


def tri_pts(t, L=L_ST):
    """Strip of t triangles, first one pointing up. Returns the 3 corners of each triangle."""
    h = L * 0.866
    out = []
    for i in range(t):
        k = i // 2
        if i % 2 == 0:
            out.append([(k * L, h), ((k + 1) * L, h), (k * L + L / 2, 0)])
        else:
            out.append([(k * L + L / 2, 0), ((k + 1) * L + L / 2, 0), ((k + 1) * L, h)])
    return out, h


def strip_w(t, L=L_ST):
    return ((t + 1) // 2) * L + (L / 2 if t % 2 == 0 else 0)


def shp_sticks_tri(n, p):
    """Row of n + p triangles made of toothpicks: 2 × triangles + 1 sticks."""
    t = n + p
    tris, h = tri_pts(t)
    s = []
    seen = set()
    for tr in tris:
        for a in range(3):
            e = tuple(sorted([tr[a], tr[(a + 1) % 3]]))
            if e not in seen:
                seen.add(e)
                s.append(stick(e[0][0] + 1, e[0][1] + 2, e[1][0] + 1, e[1][1] + 2))
    assert len(seen) == 2 * t + 1
    return strip_w(t) + 2, h + 4, s, 2 * t + 1


def shp_tri(n, p):
    """Strip of 2n - 1 + 2p filled triangles."""
    t = 2 * n - 1 + 2 * p
    L = 26
    tris, h = tri_pts(t, L)
    s = []
    for i, tr in enumerate(tris):
        s.append("<polygon points='%s' fill='%s' stroke='%s' stroke-width='2' stroke-linejoin='round'/>"
                 % (" ".join("%.1f,%.1f" % (x + 1, y + 1) for x, y in tr), FILL if i % 2 == 0 else FILL2, GREEN))
    return strip_w(t, L) + 2, h + 2, s, t


SHAPES = {
    # name: (draw, thing counted, short description of how it grows)
    "grid": shp_grid, "L": shp_L, "cross": shp_cross, "sticks_sq": shp_sticks_sq,
    "sticks_tri": shp_sticks_tri, "tri": shp_tri,
}


def thing(kind, p):
    if kind == "grid":
        return "square" if p[2] == "sq" else "dot"
    if kind in ("sticks_sq", "sticks_tri"):
        return "toothpick"
    if kind == "tri":
        return "triangle"
    return "square"


def count(kind, p, n):
    return SHAPES[kind](n, p)[3]


def pattern_svg(kind, p, figs=(1, 2, 3)):
    """Figures side by side, bottoms lined up, each with 'Figure n' under it. Sized to fit."""
    parts = [SHAPES[kind](n, p) for n in figs]
    LBW = 70                                    # width of the label 'Figure 3' at 15px bold
    gap, pad = 24, 8
    hmax = max(h for w, h, s, c in parts)
    x = pad
    out = []
    for n, (w, h, s, c) in zip(figs, parts):
        col = max(w, LBW)
        ox = x + (col - w) / 2
        oy = pad + hmax - h
        out.append("<g transform='translate(%.1f,%.1f)'>%s</g>" % (ox, oy, "".join(s)))
        out.append(text(x + col / 2, pad + hmax + 22, "Figure %d" % n, 15))
        x += col + gap
    W = int(x - gap + pad)
    H = int(pad + hmax + 30)
    lab = "growing pattern of %ss: figures %s" % (thing(kind, p), ", ".join(str(n) for n in figs))
    return svg_wrap(W, H, "".join(out), lab)


# ------------------------------------------------------------ set 1: extend a pattern with a rule
def set_extend(rnd):
    its, hard = [], []
    used = set()

    def pick(op, starts, ks):
        while True:
            s, k = rnd.choice(starts), rnd.choice(ks)
            if (op, s, k) in used or s == k:
                continue
            used.add((op, s, k))
            return s, k

    # A: add, next number
    adds = [(list(range(2, 20)), list(range(3, 10))), (list(range(2, 20)), list(range(3, 10))),
            (list(range(11, 40)), list(range(6, 13))), (list(range(20, 90, 5)), [15, 25]),
            (list(range(100, 400, 10)), [50, 120, 150]), (list(range(1100, 1600, 50)), [125, 250])]
    for starts, ks in adds:
        s, k = pick("add", starts, ks)
        xs = seq(s, "add", k, 5)
        last = xs[-2]
        q = "The rule is <b>%s</b>. What number comes next?<br>%s" % (rule_txt("add", k), show(xs[:4]))
        e = "Use the rule on the last number: %s + %s = %s." % (f(last), f(k), f(xs[-1]))
        its.append(mcq(q, f(xs[-1]), [f(v) for v in [last + 2 * k, last] + ([last + s] if s <= 2 * k else []) + ([last + k * 10] if k >= 15 else [last + k + 1, last + k - 1])], e, rnd))
    # B: subtract, next number
    for starts, ks in [(list(range(60, 100)), list(range(3, 10))), (list(range(90, 150)), list(range(6, 13))),
                       ([1000, 1200, 1500], [50, 75, 125])]:
        s, k = pick("sub", starts, ks)
        xs = seq(s, "sub", k, 5)
        last = xs[-2]
        q = "The rule is <b>%s</b>. What number comes next?<br>%s" % (rule_txt("sub", k), show(xs[:4]))
        e = "Use the rule on the last number: %s − %s = %s." % (f(last), f(k), f(xs[-1]))
        its.append(mcq(q, f(xs[-1]), [f(v) for v in [last - 2 * k, last] + ([last - k * 10] if k >= 15 else [last - k - 1, last - k + 1])], e, rnd))
    # C: multiply, next number
    for s, k, n in [(3, 2, 4), (2, 3, 4), (5, 2, 5), (1, 4, 4)]:
        used.add(("mul", s, k))
        xs = seq(s, "mul", k, n + 1)
        last, prev = xs[-2], xs[-3]
        q = "The rule is <b>%s</b>. What number comes next?<br>%s" % (rule_txt("mul", k), show(xs[:n]))
        e = ("Multiply the last number by %d: %s × %d = %s. (Adding the same jump does not work: the jumps "
             "get bigger each time.)" % (k, f(last), k, f(xs[-1])))
        its.append(mcq(q, f(xs[-1]), [f(v) for v in [last + (last - prev), last + (xs[1] - xs[0]), last + k, last * k * k]], e, rnd))
    rnd.shuffle(its)
    # D: first four numbers
    for s, op, k in [(7, "add", 6), (40, "sub", 5), (2, "mul", 3)]:
        xs = seq(s, op, k, 5)
        right = lst(xs[:4])
        wrong = [lst(xs[1:5])]
        if op == "add":
            wrong += [lst([k, 2 * k, 3 * k, 4 * k]), lst([s, 2 * s, 3 * s, 4 * s])]
            why = "Start at %d, then add %d each time: %s." % (s, k, jumps(xs[:4], op, k))
        elif op == "sub":
            wrong += [lst(seq(s, "add", k, 4)), lst([k, 2 * k, 3 * k, 4 * k])]
            why = "Start at %d, then subtract %d each time: %s." % (s, k, jumps(xs[:4], op, k))
        else:
            wrong += [lst(seq(s, "add", k, 4)), lst(seq(s, "add", s, 4))]
            why = "Start at %d, then multiply by %d each time: %s." % (s, k, jumps(xs[:4], op, k))
        why += " The start number is the 1st number, so do not use the rule on it before writing it."
        q = "Start at <b>%d</b>. The rule is <b>%s</b>. Which list shows the first four numbers?" % (s, rule_txt(op, k))
        hard.append(mcq(q, right, wrong, why, rnd))
    # E: the nth number (count the jumps)
    for s, op, k, n in [(8, "add", 5, 7), (4, "add", 9, 6), (100, "sub", 8, 8), (250, "add", 125, 9)]:
        xs = seq(s, op, k, n)
        ans = xs[-1]
        d = 1 if op == "add" else -1
        wrong = [s + d * n * k, s + d * (n - 2) * k, n * k if op == "add" else s + (n - 1) * k,
                 s + d * (n + 1) * k]
        q = "Start at <b>%s</b>. The rule is <b>%s</b>. What is the %s number in the pattern?" % (f(s), rule_txt(op, k), ordn(n))
        e = ("From the 1st number to the %s number there are %d jumps, not %d. %s %s %d × %s = %s. "
             "List: %s." % (ordn(n), n - 1, n, f(s), sign(op), n - 1, f(k), f(ans), lst(xs)))
        hard.append(mcq(q, f(ans), [f(v) for v in wrong], e, rnd))
    rnd.shuffle(hard)
    its += hard
    return {"title": "Use a rule: find the next numbers", "items": its}


# ------------------------------------------------------------ set 2: find the rule
def set_find_rule(rnd):
    its, hard = [], []
    used = set()
    # A: add rules
    for _ in range(6):
        while True:
            s, k = rnd.randint(2, 30), rnd.choice([3, 4, 5, 6, 7, 8, 9, 11, 12, 15, 20, 25])
            if s != k and (s, k) not in used and s != 2 * k and s != k + 1:
                break
        used.add((s, k))
        xs = seq(s, "add", k, 4)
        q = "Which rule makes this pattern?<br>%s" % show(xs, "…")
        e = ("Find the jump between each pair of numbers: %s. Each number is %d more than the one before, "
             "so the rule is Add %d." % (", ".join("%d − %d = %d" % (b, a, b - a) for a, b in zip(xs, xs[1:])), k, k))
        its.append(mcq(q, "Add %d" % k, ["Add %d" % s, "Subtract %d" % k, "Add %d" % (2 * k), "Add %d" % (k + 1)], e, rnd))
    # B: subtract rules
    for s, k in [(90, 8), (75, 6), (200, 15), (1000, 25)]:
        xs = seq(s, "sub", k, 4)
        q = "Which rule makes this pattern?<br>%s" % show(xs, "…")
        e = ("The numbers get smaller, so the rule subtracts. %s. Each number is %d less than the one before: Subtract %d."
             % (", ".join("%s − %s = %s" % (f(a), f(b), f(a - b)) for a, b in zip(xs, xs[1:])), k, k))
        its.append(mcq(q, "Subtract %d" % k, ["Add %d" % k, "Subtract %d" % (2 * k), "Subtract %d" % (k + 1)], e, rnd))
    # C: multiply rules (the first jump alone is a trap)
    for s, k in [(2, 3), (3, 2), (1, 5), (4, 2), (2, 4)]:
        xs = seq(s, "mul", k, 4)
        d = [b - a for a, b in zip(xs, xs[1:])]
        q = "Which rule makes this pattern?<br>%s" % show(xs, "…")
        e = ("The jumps are %s, so it is not adding the same number each time. Each number is %d times the one "
             "before: %s. The rule is Multiply by %d." % (", ".join(str(x) for x in d), k, jumps(xs, "mul", k), k))
        its.append(mcq(q, "Multiply by %d" % k, ["Add %d" % d[0], "Add %d" % d[-1], "Add %d" % k,
                                                 "Multiply by %d" % (k + 1)], e, rnd))
    rnd.shuffle(its)
    # D: a missing number in the middle
    for s, op, k, gap in [(4, "add", 5, 2), (13, "add", 12, 3), (96, "sub", 7, 2), (2, "mul", 3, 2), (5, "mul", 2, 3)]:
        xs = seq(s, op, k, 5)
        ans = xs[gap]
        prev = xs[gap - 1]
        shown = [f(x) if i != gap else "<span style='color:%s'>?</span>" % RED for i, x in enumerate(xs)]
        q = "What is the missing number?<br><b>%s</b>" % ", ".join(shown)
        if op == "mul":
            wrong = [prev + (xs[1] - xs[0]), (prev + xs[gap + 1]) // 2, prev * (k + 1), xs[-1] * k]
            e = ("The jumps grow, so look for times: %s. The rule is Multiply by %d, so the missing number is "
                 "%d × %d = %d. Check: %d × %d = %d." % (jumps(xs[:2], op, k), k, prev, k, ans, ans, k, xs[gap + 1]))
        else:
            wrong = [xs[-1] + (k if op == "add" else -k), prev + (1 if op == "add" else -1) * (k + 1),
                     prev + (1 if op == "add" else -1) * (k - 1), prev + s]
            e = ("The rule is %s (%s). So the missing number is %d %s %d = %d. Check: %d %s %d = %d."
                 % (rule_txt(op, k), jumps(xs[:2], op, k), prev, sign(op), k, ans, ans, sign(op), k, xs[gap + 1]))
        hard.append(mcq(q, f(ans), [f(v) for v in wrong], e, rnd))
    rnd.shuffle(hard)
    its += hard
    return {"title": "Find the rule and the missing number", "items": its}


# ------------------------------------------------------------ set 3: growing shape patterns
def set_shapes(rnd):
    plan = [
        ("grid", (2, 1, "dot"), "next"), ("grid", (3, 1, "sq"), "far"), ("grid", (4, 0, "dot"), "rule"),
        ("grid", (2, 2, "sq"), "which"),
        ("L", (0,), "next"), ("L", (1,), "far"), ("L", (2,), "rule"), ("L", (1,), "which"),
        ("cross", (0,), "next"), ("cross", (1,), "rule"), ("cross", (0,), "far"), ("cross", (1,), "which"),
        ("sticks_sq", (0,), "next"), ("sticks_sq", (0,), "far"), ("sticks_tri", (0,), "rule"),
        ("sticks_tri", (1,), "which"),
        ("tri", (0,), "next"), ("tri", (1,), "far"), ("tri", (0,), "rule"), ("sticks_sq", (1,), "which"),
    ]
    order = {"next": 0, "rule": 1, "far": 2, "which": 3}
    its = []
    fars = [6, 6, 8, 10, 7]
    whichs = [9, 7, 8, 12, 10]
    fi = wi = 0
    for kind, p, qk in plan:
        p = p if kind == "grid" else p[0]
        a, b, c = [count(kind, p, n) for n in (1, 2, 3)]
        k = b - a
        assert c - b == k
        w = thing(kind, p)
        F = fig(pattern_svg(kind, p))
        grow = "Each figure has %s more than the one before (%d, %d, %d)." % (pl(k, w), a, b, c)
        if qk == "next":
            ans = c + k
            q = F + "How many %ss will Figure 4 have?" % w
            e = grow + " Figure 4: %d + %d = %d." % (c, k, ans)
            cands = [c + 1, c + 2 * k, 4 * k, 4 * a, c + k + 1]
        elif qk == "far":
            n = fars[fi]; fi += 1
            ans = a + (n - 1) * k
            q = F + "How many %ss will Figure %d have?" % (w, n)
            e = grow + (" From Figure 1 to Figure %d there are %d jumps of %d: %d + %d × %d = %d."
                        % (n, n - 1, k, a, n - 1, k, ans))
            cands = ([c * 2] if n == 6 else []) + [a + n * k, a + (n - 2) * k, n * k, n * a]
        elif qk == "rule":
            ans = "Add %s" % pl(k, w)
            q = F + "Which rule tells how the pattern grows?"
            e = grow + " The rule is Add %d." % k + (" Figure 1 is only the start: %d is not the rule." % a if a != k else "")
            cands = ["Add %s" % pl(a, w), "Multiply by 2", "Add %s" % pl(1, w), "Add %s" % pl(k + 1, w), "Add %s" % pl(c, w)]
        else:
            n = whichs[wi]; wi += 1
            N = a + (n - 1) * k
            ans = "Figure %d" % n
            q = F + "If the pattern keeps going, which figure will have %d %ss?" % (N, w)
            e = (grow + " Keep adding %d: %s. Figure %d has %d %ss."
                 % (k, ", ".join(str(a + i * k) for i in range(n)), n, N, w))
            cands = ["Figure %d" % v for v in [n + 1, n - 1, N // k, n + 2]]
        if qk in ("next", "far"):
            ans = str(ans)
            cands = [str(v) for v in cands]
        its.append((order[qk], mcq(q, ans, cands, e, rnd)))
    # easy first: next figure, then the rule, then far figures, then which figure
    rnd.shuffle(its)
    its.sort(key=lambda t: t[0])
    return {"title": "Growing shape patterns", "items": [it for _, it in its]}


# ------------------------------------------------------------ set 4: features that are not in the rule
def parity(x):
    return "odd" if x % 2 else "even"


def set_features(rnd, P):
    its, hard = [], []
    # A: odd and even (add)
    ALT = ["odd, even, odd, even", "even, odd, even, odd", "all odd", "all even"]
    for s, k in [(1, 3), (6, 5), (5, 4), (8, 6), (11, 7)]:
        xs = seq(s, "add", k, 4)
        if k % 2:
            right = ALT[0] if s % 2 else ALT[1]
            why = ("%d is odd, and adding an odd number turns odd into even and even into odd. "
                   "So the numbers take turns: %s." % (k, ", ".join("%d (%s)" % (x, parity(x)) for x in xs)))
        else:
            right = ALT[2] if s % 2 else ALT[3]
            why = ("%d is even, and adding an even number never changes odd or even. %d is %s, so every "
                   "number is %s: %s." % (k, s, parity(s), parity(s), lst(xs)))
        q = "Start at <b>%d</b>. The rule is <b>Add %d</b>. Which shows the odd and even numbers in the pattern?" % (s, k)
        its.append(mcq(q, right, [x for x in ALT if x != right], why, rnd))
    # B: why does it happen?
    xs = seq(1, "add", 3, 5)
    its.append(mcq("The rule <b>Add 3</b> starting at 1 makes the pattern below. Why do the numbers take turns being odd and even?<br>%s" % show(xs, "…"),
                   "Adding 3 (odd) switches odd and even",
                   ["The rule says to switch", "The numbers get bigger", "Odd + odd is always odd"],
                   "1 is odd. Odd + odd = even (1 + 3 = 4), and even + odd = odd (4 + 3 = 7). "
                   "Every jump of 3 switches odd and even, so it keeps alternating forever.", rnd))
    xs = seq(2, "add", 4, 5)
    its.append(mcq("The rule <b>Add 4</b> starting at 2 makes the pattern below. Why is every number even?<br>%s" % show(xs, "…"),
                   "Even + even is always even",
                   ["4 is bigger than 2", "Even + even is odd", "The numbers skip by 2"],
                   "2 is even, and 4 is even. Even + even = even, so 2 + 4 = 6, 6 + 4 = 10, and every number after "
                   "that stays even.", rnd))
    xs = seq(7, "add", 10, 5)
    its.append(mcq("The rule <b>Add 10</b> starting at 7 makes the pattern below. Why does every number end in 7?<br>%s" % show(xs, "…"),
                   "Adding 10 changes only the tens",
                   ["7 is an odd number", "Adding 10 adds 1 one", "The rule says to end in 7"],
                   "10 is 1 ten and 0 ones. Adding 10 makes the tens digit go up by 1 and leaves the ones digit "
                   "alone, so it stays 7: %s." % lst(xs), rnd))
    # C: ones digits
    xs = seq(3, "add", 5, 6)
    its.append(mcq("Start at 3. The rule is <b>Add 5</b>. Which is true about the ones digits?<br>%s" % show(xs, "…"),
                   "They repeat 3, 8, 3, 8",
                   ["They are all 3", "They go up by 5 forever", "They repeat 3, 5, 3, 5"],
                   "Look only at the last digit: 3, 8, 3, 8, 3, 8. Adding 5 to a number ending in 3 gives a number "
                   "ending in 8, and adding 5 again gives a number ending in 3 (8 + 5 = 13).", rnd))
    xs = seq(1, "add", 2, 7)
    its.append(mcq("Start at 1. The rule is <b>Add 2</b>. Which is true about the ones digits?<br>%s" % show(xs, "…"),
                   "They repeat 1, 3, 5, 7, 9",
                   ["They repeat 1, 2, 1, 2", "They are all 1", "They are all even"],
                   "The ones digits go 1, 3, 5, 7, 9, then 11 ends in 1 again, so 1, 3, 5, 7, 9 repeats. "
                   "Every number is odd, because odd + even (2) is odd.", rnd))
    xs = seq(24, "add", 20, 5)
    its.append(mcq("Start at 24. The rule is <b>Add 20</b>. Which is true?<br>%s" % show(xs, "…"),
                   "Every number ends in 4",
                   ["The numbers take turns odd, even", "Every number ends in 0", "Every number is odd"],
                   "20 has 0 ones, so the ones digit never changes: %s all end in 4. They are all even too." % lst(xs), rnd))
    # D: multiples
    xs = seq(5, "add", 5, 5)
    its.append(mcq("Start at 5. The rule is <b>Add 5</b>. Which is true about every number?<br>%s" % show(xs, "…"),
                   "It is a multiple of 5",
                   ["It is odd", "It ends in 5", "It is a multiple of 10"],
                   "These are the skip-counting numbers for 5 (5 × 1, 5 × 2, 5 × 3, ...), so all are multiples of 5. "
                   "They are not all odd: 10 and 20 are even, and they end in 5 or 0.", rnd))
    xs = seq(15, "add", 10, 5)
    its.append(mcq("Start at 15. The rule is <b>Add 10</b>. Which is true about every number?<br>%s" % show(xs, "…"),
                   "It is odd and ends in 5",
                   ["It is a multiple of 10", "It is even", "It ends in 0"],
                   "Adding 10 does not change the ones digit, so every number ends in 5. A number ending in 5 is odd "
                   "(and a multiple of 5): %s." % lst(xs), rnd))
    # E: multiply rules
    xs = seq(3, "mul", 3, 5)
    hard.append(mcq("Start at 3. The rule is <b>Multiply by 3</b>. Which is true?<br>%s" % show(xs, "…"),
                    "Every number is odd",
                    ["Every number is even", "They take turns odd, even", "Every number ends in 3"],
                    "Odd × odd = odd. 3 is odd, so 3 × 3 = 9, 9 × 3 = 27, 27 × 3 = 81, and every number stays odd. "
                    "They do not all end in 3 (9, 27, 81).", rnd))
    xs = seq(5, "mul", 2, 6)
    hard.append(mcq("Start at 5. The rule is <b>Multiply by 2</b>. Which is true?<br>%s" % show(xs, "…"),
                    "After 5, every number ends in 0",
                    ["Every number ends in 5", "They take turns odd, even", "Every number is odd"],
                    "5 × 2 = 10 ends in 0. Doubling a number that ends in 0 gives another number that ends in 0 "
                    "(10, 20, 40, 80, 160), so after 5 every number ends in 0 and is even.", rnd))
    # F: which number will NOT be in the pattern?
    cases = [(2, 4, [30, 42, 50], 36), (3, 4, [19, 27, 35], 25), (1, 3, [16, 22, 25], 15),
             (5, 10, [45, 75, 105], 60), (6, 5, [26, 41, 56], 48)]
    for s, k, ins, out in cases:
        xs = seq(s, "add", k, 4)
        for v in ins:
            assert (v - s) % k == 0
        assert (out - s) % k != 0
        q = "Start at %d. The rule is <b>Add %d</b>. Which number will <b>not</b> be in the pattern?<br>%s" % (s, k, show(xs, "…"))
        prev = s + ((out - s) // k) * k
        note = {36: "Every number is even, but being even is not enough. ",
                25: "Every number is odd, but being odd is not enough. ",
                15: "The numbers take turns odd and even, so odd or even does not help here. ",
                60: "Every number ends in 5, so 60 (ending in 0) cannot be in it. ",
                48: "The ones digits repeat 6, 1, 6, 1, so 48 (ending in 8) cannot be in it. "}[out]
        why = note + ("Keep adding %d: ..., %d, %d, ... jumps right over %d. %s are all in the pattern."
                      % (k, prev, prev + k, out, ", ".join(str(v) for v in ins[:-1]) + " and " + str(ins[-1])))
        hard.append(mcq(q, str(out), [str(v) for v in ins], why, rnd))
    rnd.shuffle(its)
    rnd.shuffle(hard)
    its += hard
    return {"title": "Features of a pattern: odd, even and ones digits", "items": its}


# ------------------------------------------------------------ set 5: input/output tables and word problems
def io_svg(ins, outs, label):
    CW, LW, RH = 54, 58, 34
    n = len(ins)
    W, H = LW + CW * n + 4, RH * 2 + 4
    s = []
    for r, (name, row) in enumerate([("In", ins), ("Out", outs)]):
        y = 2 + r * RH
        s.append("<rect x='2' y='%d' width='%d' height='%d' fill='%s' stroke='%s' stroke-width='2'/>" % (y, LW, RH, FILL, GREEN))
        s.append(text(2 + LW / 2, y + RH / 2 + 6, name, 16))
        for i, v in enumerate(row):
            x = 2 + LW + i * CW
            s.append("<rect x='%d' y='%d' width='%d' height='%d' fill='#fff' stroke='%s' stroke-width='2'/>" % (x, y, CW, RH, GREEN))
            t = f(v) if isinstance(v, int) else v
            s.append(text(x + CW / 2, y + RH / 2 + 6, t, 17, col=RED if t == "?" else INK))
    return svg_wrap(W, H, "".join(s), label)


def set_words(rnd, P):
    tabs, words = [], []
    # tables: missing output
    ins, m = [2, 3, 5, 7], 4
    outs = [x * m for x in ins]
    tabs.append(mcq(fig(io_svg(ins, outs[:3] + ["?"], "input output table, rule multiply by 4")) +
                    "The rule is <b>Multiply by 4</b>. What is the missing Out number?",
                    "28", ["13", "24", "11", "35"],
                    "Use the rule on the In number below the ?: 7 × 4 = 28. (Do not just add 4 to the last Out number: "
                    "the In numbers do not go up by 1.)", rnd))
    ins, k = [6, 9, 13, 20], 15
    outs = [x + k for x in ins]
    tabs.append(mcq(fig(io_svg(ins, outs[:3] + ["?"], "input output table, rule add 15")) +
                    "The rule is <b>Add 15</b>. What is the missing Out number?",
                    "35", ["43", "300", "5", "31"],
                    "Use the rule on the In number above the ?: 20 + 15 = 35. (Do not add 15 to the last Out number.) Check another column: 13 + 15 = 28.", rnd))
    # tables: find the rule
    ins = [2, 4, 5, 8]
    tabs.append(mcq(fig(io_svg(ins, [x * 3 for x in ins], "input output table, find the rule")) +
                    "Which rule changes each In number to its Out number?",
                    "Multiply by 3", ["Add 4", "Add 6", "Multiply by 2"],
                    "Test every column, not just the first. Add 4 works for 2 → 6 but not for 4 → 12. "
                    "Multiply by 3 works for all: 2 × 3 = 6, 4 × 3 = 12, 5 × 3 = 15, 8 × 3 = 24.", rnd))
    ins = [3, 5, 8, 10]
    tabs.append(mcq(fig(io_svg(ins, [x + 7 for x in ins], "input output table, find the rule")) +
                    "Which rule changes each In number to its Out number?",
                    "Add 7", ["Add 2", "Multiply by 3", "Add 10"],
                    "Compare each In with the Out below it: 3 + 7 = 10, 5 + 7 = 12, 8 + 7 = 15, 10 + 7 = 17. "
                    "The Out numbers go up by 2 here only because the In numbers go up by 2.", rnd))
    # tables: missing input (work backward)
    ins = [4, 7, 11, "?"]
    tabs.append(mcq(fig(io_svg(ins, [13, 16, 20, 24], "input output table, rule add 9")) +
                    "The rule is <b>Add 9</b>. What is the missing In number?",
                    "15", ["33", "14", "16", "24"],
                    "Work backward: which number plus 9 makes 24? Undo adding by subtracting: 24 − 9 = 15. "
                    "Check: 15 + 9 = 24.", rnd))
    tabs.append(mcq(fig(io_svg([2, 5, 6, "?"], [6, 15, 18, 27], "input output table, rule multiply by 3")) +
                    "The rule is <b>Multiply by 3</b>. What is the missing In number?",
                    "9", ["81", "24", "30", "8"],
                    "Work backward: what number times 3 is 27? 9 × 3 = 27, so the In number is 9 (27 ÷ 3 = 9).", rnd))
    rnd.shuffle(tabs)

    def money(v):
        return "$" + f(v)

    n, he, his = P.next()
    words.append(mcq("%s has $15. %s saves $6 each week. How much money will %s have after 5 weeks?" % (n, cap(he), he),
                     money(45), [money(v) for v in [51, 39, 30, 21]],
                     "Start at $15 and add $6 five times: 15, 21, 27, 33, 39, 45. Or: $15 + 5 × $6 = $15 + $30 = $45.", rnd))
    words.append(mcq("A bean plant is 4 cm tall. It grows 3 cm each week. After how many weeks will it be 25 cm tall?",
                     "7 weeks", ["8 weeks", "6 weeks", "21 weeks"],
                     "It has to grow 25 − 4 = 21 cm. 21 ÷ 3 = 7, so 7 weeks. Check: 4, 7, 10, 13, 16, 19, 22, 25.", rnd))
    words.append(mcq("One paper cup is 9 cm tall. Each cup you stack on top adds 2 cm. How tall is a stack of 10 cups?",
                     "27 cm", ["29 cm", "20 cm", "90 cm"],
                     "The first cup is 9 cm. The other 9 cups add 2 cm each: 9 + 9 × 2 = 9 + 18 = 27 cm.", rnd))
    words.append(mcq("In a theater, the first row has 12 seats. Each row has 2 more seats than the row in front of it. "
                     "How many seats are in row 8?",
                     "26 seats", ["28 seats", "24 seats", "96 seats"],
                     "From row 1 to row 8 there are 7 jumps of 2: 12 + 7 × 2 = 26. "
                     "List: 12, 14, 16, 18, 20, 22, 24, 26.", rnd))
    words.append(mcq("One square table seats 4 people. Two tables pushed together in a line seat 6 people, and each "
                     "extra table adds 2 seats. How many people can sit at 10 tables in a line?",
                     "22 people", ["40 people", "24 people", "20 people"],
                     "The pattern is 4, 6, 8, ... (Add 2). 1 table seats 4, and the other 9 tables add 2 each: "
                     "4 + 9 × 2 = 22. It is not 10 × 4 = 40, because seats are lost where two tables touch.", rnd))
    words.append(mcq("A tank holds 1,200 liters of water. 150 liters drain out each hour. How much water is left after 6 hours?",
                     "300 liters", ["150 liters", "450 liters", "900 liters"],
                     "Subtract 150 six times: 1,200, 1,050, 900, 750, 600, 450, 300. Or: 6 × 150 = 900 drained, "
                     "and 1,200 − 900 = 300 liters left.", rnd))
    words.append(mcq("A pond has 3 lily pads on day 1. Each day the number of lily pads doubles. How many lily pads "
                     "are there on day 5?",
                     "48 lily pads", ["15 lily pads", "96 lily pads", "24 lily pads"],
                     "Doubles means Multiply by 2: day 1: 3, day 2: 6, day 3: 12, day 4: 24, day 5: 48. "
                     "Adding 3 each day (15) uses only the first jump.", rnd))
    n, he, his = P.next()
    words.append(mcq("%s puts 5 stickers on page 1 of an album. Each page has 10 more stickers than the page before. "
                     "Will any page have exactly 40 stickers?" % n,
                     "No, every page ends in 5", ["Yes, page 4", "Yes, page 8", "No, 40 is too many"],
                     "The pages have 5, 15, 25, 35, 45, ... stickers. Adding 10 never changes the ones digit, "
                     "so every number ends in 5. Page 4 has 35 and page 5 has 45, so no page has 40.", rnd))
    words.append(mcq("A school library has 1,250 books. It buys 175 new books each year. How many books will it "
                     "have after 4 years?",
                     "1,950 books", ["2,125 books", "1,775 books", "700 books"],
                     "Add 175 four times: 1,250, 1,425, 1,600, 1,775, 1,950. Or: 4 × 175 = 700, and 1,250 + 700 = 1,950.", rnd))
    n, he, his = P.next()
    words.append(mcq("On day 1, %s walks 2,000 steps. Each day %s walks 500 more steps than the day before. "
                     "How many steps does %s walk on day 6?" % (n, he, he),
                     "4,500 steps", ["5,000 steps", "4,000 steps", "3,000 steps"],
                     "From day 1 to day 6 there are 5 jumps of 500: 2,000 + 5 × 500 = 4,500. "
                     "List: 2,000, 2,500, 3,000, 3,500, 4,000, 4,500.", rnd))
    n, he, his = P.next()
    words.append(mcq("%s makes a row of squares with toothpicks. 1 square uses 4 toothpicks, 2 squares use 7, and "
                     "3 squares use 10. How many toothpicks does %s need for 12 squares?" % (n, he),
                     "37 toothpicks", ["48 toothpicks", "36 toothpicks", "40 toothpicks"],
                     "Each new square needs only 3 more toothpicks, because it shares a side. The first square uses 4, "
                     "and the other 11 squares add 3 each: 4 + 11 × 3 = 37.", rnd))
    words.append(mcq("At noon it is 68°F. The temperature drops 3°F each hour. What is the temperature at 5 p.m.?",
                     "53°F", ["50°F", "56°F", "83°F"],
                     "Noon to 5 p.m. is 5 hours. Subtract 3 five times: 68, 65, 62, 59, 56, 53. "
                     "Or: 5 × 3 = 15, and 68 − 15 = 53°F.", rnd))
    n, he, his = P.next()
    words.append(mcq("%s has $1. %s saves $4 each week. Will %s ever have exactly $30?" % (n, cap(he), he),
                     "No, the totals are always odd", ["Yes, after 7 weeks", "Yes, after 8 weeks", "No, $30 is too much"],
                     "The totals are $1, $5, $9, $13, ..., $25, $29, $33. 1 is odd, and odd + even (4) is odd, so every "
                     "total is odd. $30 is even, so it never comes up.", rnd))
    words.append(mcq("Each pizza is cut into 8 slices. 1 pizza has 8 slices, 2 pizzas have 16, and 3 pizzas have 24. "
                     "How many slices are in 7 pizzas?",
                     "56 slices", ["32 slices", "64 slices", "15 slices"],
                     "The rule is Add 8, so the number of slices is 8 times the number of pizzas: 7 × 8 = 56.", rnd))
    rnd.shuffle(words)
    return {"title": "Input/output tables and word problems", "items": tabs + words}


# ------------------------------------------------------------ lesson
def ex(title, q, s, a):
    return ("<div class='sn-ex'><span class='sn-ex-t'>%s</span><p class='sn-ex-q'>%s</p>"
            "<p class='sn-ex-s'>%s</p><p class='sn-ex-a'>Answer: %s</p></div>" % (title, q, s, a))


def table(head, rows, cls="sn-table"):
    h = "".join("<th>%s</th>" % x for x in head)
    b = "".join("<tr>" + "".join("<td>%s</td>" % c for c in r) + "</tr>" for r in rows)
    return "<div class='sn-tw'><table class='%s'><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>" % (cls, h, b)


def body_html():
    return (
        "<h2>A rule makes the pattern</h2>"
        "<p>A pattern starts with a <b>start number</b> (or a first figure). A <b>rule</b> tells you how to get "
        "the next one, such as <b>Add 3</b>, <b>Subtract 5</b> or <b>Multiply by 2</b>. "
        "Use the rule on the <b>last</b> number, one step at a time.</p>" +
        ex("Number pattern", "Start at 1. The rule is Add 3. What are the first five numbers?",
           "1 is the start. 1 + 3 = 4, 4 + 3 = 7, 7 + 3 = 10, 10 + 3 = 13.", "1, 4, 7, 10, 13") +
        ex("Find the rule", "3, 6, 12, 24, ...",
           "The jumps are 3, 6, 12, so it is not adding the same number. Each number is 2 times the one before.",
           "Multiply by 2") +
        "<h2>Shape patterns grow by the same amount</h2>"
        "<p>Count the pieces in each figure, then find how many are added each time.</p>"
        "<figure class='sn-fig'>" + pattern_svg("L", 0) +
        "<figcaption>3, 5, 7 squares: each figure adds 2 squares (one on each arm). Figure 4 has 9. "
        "Figure 6 has 3 + 5 × 2 = 13, because there are 5 jumps from Figure 1 to Figure 6.</figcaption></figure>"
        "<h2>Look for features the rule does not tell you</h2>"
        "<p>The rule Add 3 says nothing about odd and even, but the numbers <b>take turns</b>: "
        "1, 4, 7, 10, 13 are odd, even, odd, even, odd. The reason: 3 is odd, and adding an odd number "
        "switches odd to even and even to odd. So it keeps alternating forever.</p>" +
        table(["Rule and start", "Pattern", "Feature", "Why"], [
            ["Add 3, start at 1", "1, 4, 7, 10, 13", "odd, even, odd, even", "odd + odd = even, even + odd = odd"],
            ["Add 4, start at 2", "2, 6, 10, 14, 18", "all even", "even + even = even"],
            ["Add 10, start at 7", "7, 17, 27, 37", "always ends in 7", "adding 10 changes only the tens"],
            ["Add 5, start at 3", "3, 8, 13, 18, 23", "ones digits 3, 8, 3, 8", "8 + 5 = 13 ends in 3 again"],
        ]) +
        "<h2>Common mistakes</h2>" +
        table(["Mistake", "What to do instead"], [
            ["Using the rule on the start number first (start 7, Add 6: 13, 19, 25)", "The start number is the 1st number: 7, 13, 19, 25"],
            ["Counting jumps wrong (7th number = start + 7 jumps)", "From the 1st to the 7th number there are 6 jumps"],
            ["Checking only the first jump (3, 6, 12, 24 is Add 3)", "Check every jump. Growing jumps mean multiply"],
            ["Doubling Figure 3 to get Figure 6", "Figure 1 is a start, not a jump. Add the rule again and again"],
            ["Thinking every odd number is in an odd pattern (3, 7, 11, ...)", "9 is odd but is skipped: test it with the rule"],
        ])
    )


FAQ = [
    {"q": "What is a number pattern in 4th grade math?",
     "a": "It is a list of numbers made by a rule, such as Start at 1 and Add 3: 1, 4, 7, 10, 13. Students extend the pattern, find the rule, and describe features the rule does not say, like odd and even numbers taking turns."},
    {"q": "How do you find the rule of a pattern?",
     "a": "Find the jump between each pair of numbers. If every jump is the same, the rule adds (or subtracts) that number; if the jumps keep growing, try multiplying, as in 2, 6, 18, 54 (Multiply by 3)."},
    {"q": "Why does the rule Add 3 make odd and even numbers alternate?",
     "a": "3 is odd, and adding an odd number changes odd to even and even to odd. So 1, 4, 7, 10, 13 will keep switching between odd and even forever."},
    {"q": "What does 4.OA.C.5 mean?",
     "a": "It is the Common Core Grade 4 standard for making number or shape patterns that follow a given rule and noticing features of the pattern that the rule does not state, then explaining informally why they happen."},
]


def balance(sets, rnd):
    """Spread the correct answers evenly over the 4 positions in every set."""
    for s in sets:
        targets = [0, 1, 2, 3] * 5
        rnd.shuffle(targets)
        for it, t in zip(s["items"], targets):
            c = it["c"]
            c[it["a"]], c[t] = c[t], c[it["a"]]
            it["a"] = t


def gen_patterns():
    rnd = random.Random(117)
    P = People(rnd)
    sets = [set_extend(rnd), set_find_rule(rnd), set_shapes(rnd), set_features(rnd, P), set_words(rnd, P)]
    balance(sets, rnd)
    seen = set()
    for s in sets:
        assert len(s["items"]) == 20, (s["title"], len(s["items"]))
        for it in s["items"]:
            assert len(set(it["c"])) == 4, it
            k = it["q"] + "|" + "|".join(sorted(it["c"]))
            assert k not in seen, it["q"]
            seen.add(k)
    return {
        "country": "us", "subject": "math", "grade": "grade-4", "slug": "number-shape-patterns", "sort": 17,
        "updated": UPDATED, "pdf_url": "",
        "title": "Number and Shape Patterns",
        "seo_title": "Grade 4 Number and Shape Patterns Worksheets: Rules, Growing Patterns and Odd/Even Features",
        "short_title": "Number and shape patterns",
        "domain": "Operations and Algebraic Thinking",
        "standard_code": "4.OA.C.5",
        "standard_url": "https://www.thecorestandards.org/Math/Content/4/OA/C/5/",
        "standard_text": "Generate a number or shape pattern that follows a given rule. Identify apparent features of the pattern that were not explicit in the rule itself. For example, given the rule “Add 3” and the starting number 1, generate terms in the resulting sequence and observe that the terms appear to alternate between odd and even numbers. Explain informally why the numbers will continue to alternate in this way.",
        "meta_desc": "Free Grade 4 pattern worksheets: extend number patterns with add, subtract and multiply rules, find the rule, growing shape patterns, odd and even features, input/output tables and word problems. 100 practice questions with step-by-step answers.",
        "key_big": "Use the rule on the last number, one step at a time. Then look for what the rule does not say.",
        "key_sub": "Start at 1 and Add 3: 1, 4, 7, 10, 13. The numbers take turns odd and even, because adding an odd number switches odd and even. From the 1st to the 7th number there are 6 jumps.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }


def mark_large(u, pattern):
    """Tag pictures that must print larger so their labels stay readable."""
    rx = re.compile(r"<svg (?=[^>]*aria-label='" + pattern + ")")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u


if __name__ == "__main__":
    u = gen_patterns()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        mark_large(u, "growing pattern")
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
