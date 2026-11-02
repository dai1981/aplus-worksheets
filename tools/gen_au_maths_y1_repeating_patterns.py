# -*- coding: utf-8 -*-
"""
AU Year 1 Maths (Australian Curriculum v9.0): repeating patterns.
AC9M1A02: recognise, continue and create repeating patterns with numbers, symbols,
shapes and objects, identifying the repeating unit.
  python3 tools/gen_au_maths_y1_repeating_patterns.py
Every pattern is a list of tokens built from its repeating unit. Every answer, every wrong
answer and every picture is computed from that list and checked in code:
  - "what comes next" / "what is missing" answers are read from the unit,
  - wrong rows in "which is a pattern" are checked to have NO repeating unit,
  - in "which bead is wrong" only one bead can be changed to make a pattern.
Colour-only patterns use red, yellow and blue (they stay different in black-and-white print).
HTML attributes use single quotes (no backslashes in the JSON).
"""
import json, math, os, random, re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "au", "maths", "year-1")
UPDATED = "2026-11-02"
GREEN = "#006633"
FILL = "#e8f3ec"
RED_INK = "#c0392b"
GREY = "#9a9a9a"
INK = "#2b2b2b"
FONT = "Arial, Helvetica, sans-serif"
COLOURS = {"red": "#d64535", "yellow": "#f4c430", "blue": "#2e6da4", "green": "#3a9a4a"}
PLAIN = ["red", "yellow", "blue"]                  # colour-only patterns
SHAPES = ["circle", "square", "triangle", "star"]
OBJECTS = ["shell", "starfish", "leaf", "apple"]
ARROW = {"up": "↑", "down": "↓", "left": "←", "right": "→"}
GIRLS = ["Charlotte", "Isla", "Mia", "Amelia", "Ava", "Harper", "Chloe", "Ruby", "Mei", "Zara", "Matilda", "Sienna", "Grace"]
BOYS = ["Oliver", "Jack", "Noah", "William", "Leo", "Lachlan", "Liam", "Aarav", "Kai", "Cooper", "Ethan"]


# ------------------------------------------------------------ tokens
# "c:red:circle" coloured shape, "o:shell" object, "n:3" number, "l:A" letter,
# "a:up" arrow, "w:clap" word, "b:red" bead, "f:red" flag
def name(tok, mode=None):
    p = tok.split(":")
    if p[0] == "c":
        return {"colour": p[1], "shape": p[2]}.get(mode, p[1] + " " + p[2])
    if p[0] == "a":
        return ARROW[p[1]]
    return p[1]


def names(toks, mode=None):
    return ", ".join(name(t, mode) for t in toks)


def build(unit, n):
    return [unit[i % len(unit)] for i in range(n)]


def period(seq):
    """Smallest repeating unit length k with at least 2 full units shown, else None."""
    for k in range(1, len(seq) // 2 + 1):
        if all(seq[i] == seq[i % k] for i in range(len(seq))):
            return k
    return None


def is_rotation(a, b):
    return len(a) == len(b) and any(a[i:] + a[:i] == b for i in range(len(a)))


def from_structure(struct, pool, rnd):
    """'ABB' + pool -> unit with distinct tokens for distinct letters."""
    letters = sorted(set(struct))
    pick = rnd.sample(pool, len(letters))
    m = dict(zip(letters, pick))
    return [m[ch] for ch in struct]


def pool_for(mode, rnd, n_needed=4):
    if mode == "colour":
        sh = rnd.choice(SHAPES)
        return ["c:%s:%s" % (c, sh) for c in PLAIN]
    if mode == "shape":
        col = rnd.choice(list(COLOURS))
        return ["c:%s:%s" % (col, s) for s in SHAPES]
    if mode == "both":
        cols = rnd.sample(list(COLOURS), 4)
        shs = rnd.sample(SHAPES, 4)
        return ["c:%s:%s" % (c, s) for c, s in zip(cols, shs)]
    if mode == "obj":
        return ["o:" + o for o in OBJECTS]
    if mode == "bead":
        return ["b:" + c for c in PLAIN]
    if mode == "flag":
        return ["f:" + c for c in PLAIN]
    raise ValueError(mode)


def outsiders(unit, mode, pool):
    """Things not in the pattern (a new colour or a new shape), most likely first."""
    out = [t for t in pool if t not in unit]
    if mode in ("colour", "shape", "both"):
        p = unit[0].split(":")
        if mode == "colour":
            out += ["c:green:" + p[2]] if "c:green:" + p[2] not in unit else []
        if mode == "both":
            for t in unit:
                c, s = t.split(":")[1:]
                for t2 in unit:
                    c2, s2 = t2.split(":")[1:]
                    if c != c2:
                        out.append("c:%s:%s" % (c, s2))
            out = [t for t in out if t not in unit]
    if mode == "bead" or mode == "flag":
        out.append(mode[0] + ":green")
    seen, res = set(), []
    for t in out:
        if t not in seen:
            seen.add(t)
            res.append(t)
    return res


# ------------------------------------------------------------ question helpers
def mcq(q, correct, cands, e):
    correct = str(correct)
    seen = {correct}
    pick = []
    for c in cands:
        c = str(c)
        if c in seen or not c or c.startswith("-") or c == "0":
            continue
        seen.add(c)
        pick.append(c)
        if len(pick) == 3:
            break
    assert len(pick) == 3, (q, correct, cands)
    return {"q": q, "c": [correct] + pick, "a": 0, "e": e}


def abcd_item(prompt, builder, right, wrong, e):
    assert len(wrong) == 3 and right not in wrong and len({repr(w) for w in wrong}) == 3
    return {"q": "", "c": ["A", "B", "C", "D"], "a": 0, "e": e, "_abcd": (prompt, builder, right, wrong)}


class People:
    def __init__(self, rnd):
        self.pool = [(n, "she", "her") for n in GIRLS] + [(n, "he", "his") for n in BOYS]
        rnd.shuffle(self.pool)
        self.i = 0

    def next(self):
        p = self.pool[self.i % len(self.pool)]
        self.i += 1
        return p


def fig(svg):
    return "<div class='qfig'>" + svg + "</div>"


def svg_wrap(w, h, body, label, large=False):
    return ("<svg %sxmlns='http://www.w3.org/2000/svg' viewBox='0 0 %d %d' width='%d' height='%d' "
            "role='img' aria-label='%s'><g font-family='%s'>%s</g></svg>"
            % ("data-pf='lg' " if large else "", w, h, w, h, label, FONT, body))


def text(x, y, t, fs=16, anchor="middle", col=INK):
    return ("<text x='%.1f' y='%.1f' font-size='%d' font-weight='700' fill='%s' text-anchor='%s'>%s</text>"
            % (x, y, fs, col, anchor, t))


def table(head, rows):
    h = "".join("<th>%s</th>" % x for x in head)
    b = "".join("<tr>" + "".join("<td>%s</td>" % c for c in r) + "</tr>" for r in rows)
    return "<div class='sn-tw'><table class='sn-table'><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>" % (h, b)


def ex(title, q, s, a):
    return ("<div class='sn-ex'><span class='sn-ex-t'>%s</span><p class='sn-ex-q'>%s</p>"
            "<p class='sn-ex-s'>%s</p><p class='sn-ex-a'>Answer: %s</p></div>" % (title, q, s, a))


# ------------------------------------------------------------ drawing
def shape(kind, col, cx, cy, c):
    f = COLOURS[col]
    st = "stroke='%s' stroke-width='1.6' stroke-linejoin='round'" % INK
    if kind == "circle":
        return "<circle cx='%.1f' cy='%.1f' r='%.1f' fill='%s' %s/>" % (cx, cy, 0.37 * c, f, st)
    if kind == "square":
        a = 0.64 * c
        return "<rect x='%.1f' y='%.1f' width='%.1f' height='%.1f' fill='%s' %s/>" % (cx - a / 2, cy - a / 2, a, a, f, st)
    if kind == "triangle":
        h, b = 0.66 * c, 0.78 * c
        return ("<polygon points='%.1f,%.1f %.1f,%.1f %.1f,%.1f' fill='%s' %s/>"
                % (cx, cy - h / 2, cx + b / 2, cy + h / 2, cx - b / 2, cy + h / 2, f, st))
    if kind == "star":
        pts = []
        for k in range(10):
            rr = 0.45 * c if k % 2 == 0 else 0.19 * c
            a = -math.pi / 2 + k * math.pi / 5
            pts.append("%.1f,%.1f" % (cx + rr * math.cos(a), cy + 0.05 * c + rr * math.sin(a)))
        return "<polygon points='%s' fill='%s' %s/>" % (" ".join(pts), f, st)
    raise ValueError(kind)


def obj(kind, cx, cy, c):
    s = c / 40.0
    if kind == "shell":
        return ("<path d='M %.1f %.1f Q %.1f %.1f %.1f %.1f Z' fill='#f4d7b5' stroke='#a0623a' stroke-width='1.5'/>"
                % (cx - 15 * s, cy + 10 * s, cx, cy - 26 * s, cx + 15 * s, cy + 10 * s)
                + "".join("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='#a0623a' stroke-width='1.1'/>"
                          % (cx, cy + 10 * s, cx + dx * s, cy - 6 * s) for dx in (-9, -3, 3, 9)))
    if kind == "starfish":
        pts = []
        for k in range(10):
            rr = (17 if k % 2 == 0 else 7) * s
            a = -math.pi / 2 + k * math.pi / 5
            pts.append("%.1f,%.1f" % (cx + rr * math.cos(a), cy + 1.5 * s + rr * math.sin(a)))
        return ("<polygon points='%s' fill='#f2a65a' stroke='#a3561c' stroke-width='1.5' stroke-linejoin='round'/>"
                % " ".join(pts))
    if kind == "leaf":
        return ("<path d='M %.1f %.1f Q %.1f %.1f %.1f %.1f Q %.1f %.1f %.1f %.1f Z' fill='#7cbf6a' stroke='#2f6b2a' stroke-width='1.5'/>"
                "<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='#2f6b2a' stroke-width='1.2'/>"
                % (cx - 14 * s, cy + 12 * s, cx - 14 * s, cy - 14 * s, cx + 14 * s, cy - 14 * s,
                   cx + 14 * s, cy + 12 * s, cx - 14 * s, cy + 12 * s,
                   cx - 14 * s, cy + 12 * s, cx + 9 * s, cy - 9 * s))
    if kind == "apple":
        return ("<circle cx='%.1f' cy='%.1f' r='%.1f' fill='#d64535' stroke='#7a1f16' stroke-width='1.5'/>"
                "<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='#6b4a2a' stroke-width='2.2'/>"
                "<ellipse cx='%.1f' cy='%.1f' rx='%.1f' ry='%.1f' fill='#3a9a4a'/>"
                % (cx, cy + 3 * s, 13 * s, cx, cy - 9 * s, cx + 2 * s, cy - 16 * s,
                   cx + 7 * s, cy - 13 * s, 5 * s, 2.5 * s))
    raise ValueError(kind)


def arrow(d, cx, cy, c):
    L = 0.36 * c
    pts = [(0, -L), (0.55 * L, -0.1 * L), (0.2 * L, -0.1 * L), (0.2 * L, L), (-0.2 * L, L), (-0.2 * L, -0.1 * L),
           (-0.55 * L, -0.1 * L)]
    ang = {"up": 0, "right": 90, "down": 180, "left": 270}[d]
    a = math.radians(ang)
    p = ["%.1f,%.1f" % (cx + x * math.cos(a) - y * math.sin(a), cy + x * math.sin(a) + y * math.cos(a)) for x, y in pts]
    return "<polygon points='%s' fill='%s' stroke='%s' stroke-width='1' stroke-linejoin='round'/>" % (" ".join(p), GREEN, GREEN)


def box(x, y, w, h):
    return ("<rect x='%.1f' y='%.1f' width='%.1f' height='%.1f' rx='5' fill='#ffffff' stroke='%s' stroke-width='1.6'/>"
            % (x, y, w, h, GREEN))


def gap_box(x, y, w, h, round_=False):
    if round_:
        r = min(w, h) * 0.37
        g = ("<circle cx='%.1f' cy='%.1f' r='%.1f' fill='%s' stroke='%s' stroke-width='1.6' stroke-dasharray='4 3'/>"
             % (x + w / 2, y + h / 2, r, FILL, GREEN))
    else:
        g = ("<rect x='%.1f' y='%.1f' width='%.1f' height='%.1f' rx='5' fill='%s' stroke='%s' stroke-width='1.6' "
             "stroke-dasharray='4 3'/>" % (x + 2, y + 2, w - 4, h - 4, FILL, GREEN))
    return g + text(x + w / 2, y + h / 2 + 7, "?", 20, col=RED_INK)


def cell_w(tokens, c):
    return c + 22 if any(t.startswith("w:") for t in tokens) else c


def token(t, x, y, w, c):
    """Draw token t in the cell at (x, y), width w, height c."""
    cx, cy = x + w / 2.0, y + c / 2.0
    p = t.split(":")
    if t == "?":
        return gap_box(x, y, w, c)
    if p[0] == "c":
        return shape(p[2], p[1], cx, cy, c)
    if p[0] == "o":
        return obj(p[1], cx, cy, c)
    if p[0] == "b":
        return "<circle cx='%.1f' cy='%.1f' r='%.1f' fill='%s' stroke='%s' stroke-width='1.6'/>" % (cx, cy, 0.37 * c, COLOURS[p[1]], INK)
    if p[0] == "f":
        return ("<polygon points='%.1f,%.1f %.1f,%.1f %.1f,%.1f' fill='%s' stroke='%s' stroke-width='1.6' stroke-linejoin='round'/>"
                % (x + 3, y + 3, x + w - 3, y + 3, cx, y + c - 2, COLOURS[p[1]], INK))
    if p[0] == "a":
        return box(x + 2, y + 2, w - 4, c - 4) + arrow(p[1], cx, cy, c)
    if p[0] in ("n", "l"):
        return box(x + 2, y + 2, w - 4, c - 4) + text(cx, cy + 0.2 * c, p[1], max(16, int(0.5 * c)))
    if p[0] == "w":
        return box(x + 2, y + 2, w - 4, c - 4) + text(cx, cy + 5, p[1], 15)
    raise ValueError(t)


def row_body(tokens, x0, y0, c=40, gap=4):
    """A row of tokens; beads get a string, flags get a rope. Returns body, w, h."""
    w = cell_w(tokens, c)
    n = len(tokens)
    W = n * w + (n - 1) * gap
    s = []
    kind = next((t[0] for t in tokens if t != "?"), "")
    if kind == "b":
        s.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='2'/>"
                 % (x0 - 4, y0 + c / 2.0, x0 + W + 4, y0 + c / 2.0, "#8a6a4a"))
    if kind == "f":
        s.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='2'/>"
                 % (x0 - 4, y0 + 2, x0 + W + 4, y0 + 2, "#8a6a4a"))
    for i, t in enumerate(tokens):
        x = x0 + i * (w + gap)
        if t == "?" and kind == "b":
            s.append(gap_box(x, y0, w, c, round_=True))
        else:
            s.append(token(t, x, y0, w, c))
    return "".join(s), W, c


def row_svg(tokens, label="a repeating pattern", c=40):
    body, w, h = row_body(tokens, 6, 4, c)
    return svg_wrap(w + 12, h + 8, body, label, large=len(tokens) > 4)


def numbered_svg(tokens, label):
    """Row with position numbers 1, 2, 3 ... under each thing."""
    c, gap = 36, 4
    body, w, h = row_body(tokens, 6, 4, c, gap)
    cw = cell_w(tokens, c)
    nums = "".join(text(6 + i * (cw + gap) + cw / 2.0, 4 + c + 18, str(i + 1), 14, col=GREY) for i in range(len(tokens)))
    return svg_wrap(w + 12, h + 28, body + nums, label, large=True)


def units_svg(pattern, options):
    """The pattern on top, then four repeating-unit choices A-D (two on each line)."""
    top, tw, th = row_body(pattern, 6, 4, 36)
    oc = 30
    sizes = [row_body(o, 0, 0, oc)[1:] for o in options]
    colw = max(w for w, h in sizes) + 36
    W = max(tw + 12, 2 * colw + 10)
    y1 = th + 18
    s = [top, "<line x1='4' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='1'/>" % (th + 10, W - 4, th + 10, GREY)]
    for k, o in enumerate(options):
        r, cl = divmod(k, 2)
        x, y = 6 + cl * (colw + 4), y1 + r * (oc + 12)
        s.append(text(x + 8, y + oc / 2.0 + 6, "ABCD"[k], 18, "start"))
        s.append("<rect x='%.1f' y='%.1f' width='%.1f' height='%.1f' rx='6' fill='none' stroke='%s' stroke-width='1.2' "
                 "stroke-dasharray='4 3'/>" % (x + 28, y - 4, sizes[k][0] + 8, oc + 8, GREY))
        s.append(row_body(o, x + 32, y, oc)[0])
    H = y1 + 2 * (oc + 12)
    return svg_wrap(W, H, "".join(s), "a pattern and four choices labelled A to D", large=True)


def rows_svg(rows):
    """Four rows labelled A to D, one under the other."""
    c, gap = 30, 4
    s = []
    W = 0
    for k, r in enumerate(rows):
        y = 6 + k * (c + 10)
        s.append(text(8, y + c / 2.0 + 6, "ABCD"[k], 18, "start"))
        body, w, h = row_body(r, 34, y, c, gap)
        s.append(body)
        W = max(W, 34 + w + 8)
        if k:
            s.append("<line x1='4' y1='%d' x2='%%d' y2='%d' stroke='%s' stroke-width='0.8'/>" % (y - 5, y - 5, "#dddddd"))
    s = [x.replace("%d", str(W - 4)) if "%d" in x else x for x in s]
    return svg_wrap(W, 6 + 4 * (c + 10) - 4, "".join(s), "four rows labelled A to D", large=True)


# ------------------------------------------------------------ question makers
def say_unit(unit, mode):
    return "<i>%s</i>" % names(unit, mode)


def next_item(unit, mode, pool, L, its, prompt="What comes next?", pre=""):
    seq = build(unit, L)
    k = len(unit)
    ans = unit[L % k]
    r = L % k
    cands = [seq[L - 2], seq[L - 1], unit[0], unit[(L + 1) % k]] + outsiders(unit, mode, pool)
    if r == 0:
        e = "The repeating unit is %s. The last unit is finished, so start it again: <b>%s</b>." % (say_unit(unit, mode), name(ans, mode))
    else:
        e = ("The repeating unit is %s. The last unit so far is %s. Next comes <b>%s</b>."
             % (say_unit(unit, mode), names(unit[:r], mode), name(ans, mode)))
    q = fig(row_svg(seq + ["?"])) + pre + prompt
    its.append(mcq(q, name(ans, mode), [name(t, mode) for t in cands if t != ans], e))


def next_two(unit, mode, pool, L, its, pre=""):
    seq = build(unit, L)
    k = len(unit)
    a, b = unit[L % k], unit[(L + 1) % k]
    ans = names([a, b], mode)
    out = outsiders(unit, mode, pool)
    cands = [names([b, a], mode), names([unit[0], unit[1 % k]], mode) if L % k else names([unit[1], unit[2 % k]], mode),
             names([seq[L - 2], seq[L - 1]], mode), names([a, out[0]], mode), names([out[0], b], mode)]
    e = ("The repeating unit is %s. Keep saying it: next comes %s, then %s. Answer: <b>%s</b>."
         % (say_unit(unit, mode), name(a, mode), name(b, mode), ans))
    q = fig(row_svg(seq + ["?", "?"])) + pre + "What are the next two?"
    its.append(mcq(q, ans, cands, e))


def gap_item(unit, mode, pool, L, p, its, pre=""):
    seq = build(unit, L)
    ans = seq[p]
    shown = seq[:p] + ["?"] + seq[p + 1:]
    cands = [seq[p - 1], seq[p + 1]] + [t for t in unit if t != ans] + outsiders(unit, mode, pool)
    e = ("The repeating unit is %s. Say it along the row from the start. The gap gets <b>%s</b>."
         % (say_unit(unit, mode), name(ans, mode)))
    q = fig(row_svg(shown)) + pre + "What is missing?"
    its.append(mcq(q, name(ans, mode), [name(t, mode) for t in cands if t != ans], e))


def two_gaps(unit, mode, pool, L, p1, p2, its, pre=""):
    seq = build(unit, L)
    a, b = seq[p1], seq[p2]
    shown = [("?" if i in (p1, p2) else t) for i, t in enumerate(seq)]
    ans = names([a, b], mode)
    out = outsiders(unit, mode, pool)
    cands = [names([b, a], mode), names([seq[p1 - 1], seq[p2 - 1]], mode), names([seq[p1 + 1], seq[p2 + 1]], mode),
             names([a, out[0]], mode), names([out[0], b], mode)]
    e = ("The repeating unit is %s. Say it along the row. The first gap is %s and the second gap is %s. "
         "Answer: <b>%s</b>." % (say_unit(unit, mode), name(a, mode), name(b, mode), ans))
    q = fig(row_svg(shown)) + pre + "What goes in the two gaps? Read from left to right."
    its.append(mcq(q, ans, cands, e))


def wrong_units(unit, rnd, pool):
    """Wrong repeating units: too short, too long, starts in the wrong place, one thing changed."""
    k = len(unit)
    c = [unit[:-1], unit + [unit[0]], unit[1:]]
    for i in range(k):
        for t in pool:
            if t != unit[i]:
                c.append(unit[:i] + [t] + unit[i + 1:])
    res = []
    for o in c:
        if not o or o == unit or is_rotation(o, unit) or o in res:
            continue
        if len(o) % k == 0 and o == build(unit, len(o)):
            continue
        res.append(o)
    head = res[:3]
    rest = res[3:]
    rnd.shuffle(rest)
    # keep too short and too long; the third is "wrong start" (or a changed one)
    return head[:2] + [head[2] if rnd.random() < 0.5 else rest[0]]


def broken_rows(unit, pool, n, rnd):
    """Rows that are NOT repeating patterns: one thing swapped, growing, unit changes halfway."""
    seq = build(unit, n)
    rows = []
    for _ in range(40):
        i = rnd.randrange(len(unit), n)
        t = rnd.choice([x for x in pool if x != seq[i]][:3])
        r = seq[:i] + [t] + seq[i + 1:]
        if period(r) is None and r not in rows:
            rows.append(r)
            break
    a, b = unit[0], next(t for t in unit if t != unit[0])
    grow = []
    j = 1
    while len(grow) < n:
        grow += [a] + [b] * j
        j += 1
    grow = grow[:n]
    if period(grow) is None and grow not in rows:
        rows.append(grow)
    half = n // 2
    other = list(reversed(unit)) if list(reversed(unit)) != unit and not is_rotation(list(reversed(unit)), unit) else [a, a, b]
    mix = seq[:half] + build(other, n - half)
    if period(mix) is None and mix not in rows:
        rows.append(mix)
    for _ in range(40):
        if len(rows) >= 3:
            break
        r = seq[:]
        i, j2 = rnd.sample(range(len(unit), n), 2)
        r[i], r[j2] = r[j2], r[i]
        if period(r) is None and r not in rows:
            rows.append(r)
    assert len(rows) >= 3, unit
    return rows[:3]


# ============================================================ set 1: what comes next
def set_next(rnd):
    its = []
    specs = [("colour", "AB"), ("colour", "AB"), ("shape", "AB"), ("shape", "AB"), ("obj", "AB"),
             ("colour", "ABB"), ("shape", "AAB"), ("shape", "ABB"), ("obj", "AAB"), ("colour", "AAB"),
             ("colour", "ABC"), ("shape", "ABC"), ("shape", "ABC"), ("both", "AB"), ("both", "ABC"),
             ("colour", "AABB"), ("shape", "AABB")]
    used = set()
    for mode, st in specs:
        for _ in range(50):
            pool = pool_for(mode, rnd)
            unit = from_structure(st, pool, rnd)
            if names(unit, mode) not in used:
                break
        used.add(names(unit, mode))
        k = len(unit)
        r = len(its) % k                     # where the row stops inside the unit (varies)
        L = (3 * k if k == 2 else 2 * k) + (r if k < 4 else r % 2)   # at most 10 boxes
        next_item(unit, mode, pool, L, its)
    for mode, st in [("colour", "AB"), ("shape", "ABB"), ("both", "ABC")]:
        pool = pool_for(mode, rnd)
        unit = from_structure(st, pool, rnd)
        k = len(unit)
        L = 2 * k + rnd.randrange(1, k) if k > 2 else 7
        next_two(unit, mode, pool, L, its)
    assert len(its) == 20, len(its)
    return {"title": "What comes next? Shapes and colours", "items": its}


# ============================================================ set 2: find the repeating unit
def set_unit(rnd):
    its = []
    specs = [("colour", "AB"), ("shape", "AB"), ("obj", "AB"), ("colour", "ABB"), ("shape", "AAB"),
             ("obj", "ABB"), ("shape", "ABC"), ("colour", "ABC"), ("both", "ABC"), ("shape", "AABB")]
    for mode, st in specs:
        pool = pool_for(mode, rnd)
        unit = from_structure(st, pool, rnd)
        k = len(unit)
        n = 3 * k if 3 * k <= 10 else 2 * k
        pat = build(unit, n)
        wrong = wrong_units(unit, rnd, pool)
        e = ("The part that repeats is %s. Then it starts again. So the repeating unit is <b>{L}</b>."
             % say_unit(unit, mode))
        its.append(abcd_item("What is the repeating unit?", units_svg, unit, wrong, e))
        its[-1]["_top"] = pat
    # how many things in the unit
    for mode, st in [("colour", "ABB"), ("shape", "ABC"), ("obj", "AAB"), ("colour", "AABB"), ("both", "AB")]:
        pool = pool_for(mode, rnd)
        unit = from_structure(st, pool, rnd)
        k = len(unit)
        n = 3 * k if 3 * k <= 10 else 2 * k
        pat = build(unit, n)
        diff = len(set(unit))
        q = fig(row_svg(pat)) + "How many things are in the repeating unit?"
        e = ("The repeating unit is %s. It has <b>%d</b> things. Count each one, even if two are the same."
             % (say_unit(unit, mode), k))
        its.append(mcq(q, k, [diff, k - 1, k + 1, n], e))
    # how many times does the unit repeat
    for mode, st, times in [("shape", "AB", 4), ("colour", "ABC", 3), ("obj", "ABB", 3), ("both", "AB", 5),
                            ("shape", "AAB", 2)]:
        pool = pool_for(mode, rnd)
        unit = from_structure(st, pool, rnd)
        k = len(unit)
        pat = build(unit, k * times)
        q = fig(row_svg(pat)) + "The repeating unit is %s. How many times does it repeat?" % names(unit, mode)
        e = ("Put a loop around each %s. There are <b>%d</b> units. There are %d things in all, but that is not the answer."
             % (names(unit, mode), times, k * times))
        its.append(mcq(q, times, [k * times, times + 1, times - 1, k], e))
    assert len(its) == 20, len(its)
    return {"title": "Find the repeating unit", "items": its}


# ============================================================ set 3: missing piece in the middle
def set_gaps(rnd):
    its = []
    specs = [("colour", "AB"), ("shape", "AB"), ("obj", "AB"), ("colour", "ABB"), ("shape", "ABB"),
             ("obj", "AAB"), ("colour", "AAB"), ("shape", "AAB"), ("colour", "ABC"), ("shape", "ABC"),
             ("both", "AB"), ("both", "ABB"), ("both", "ABC"), ("shape", "AABB"), ("colour", "AABB"),
             ("obj", "ABC")]
    for mode, st in specs:
        pool = pool_for(mode, rnd)
        unit = from_structure(st, pool, rnd)
        k = len(unit)
        L = min(3 * k, 9) if k < 4 else 8
        p = rnd.randint(k, L - 2)          # after one full unit, not at the end
        gap_item(unit, mode, pool, L, p, its)
    for mode, st in [("colour", "ABB"), ("shape", "ABC"), ("both", "AAB"), ("obj", "AABB")]:
        pool = pool_for(mode, rnd)
        unit = from_structure(st, pool, rnd)
        k = len(unit)
        L = 9 if k < 4 else 8
        p1 = rnd.randint(k, L - 4)
        p2 = rnd.randint(p1 + 2, L - 2)
        two_gaps(unit, mode, pool, L, p1, p2, its)
    assert len(its) == 20, len(its)
    return {"title": "What is missing in the middle?", "items": its}


# ============================================================ set 4: numbers and symbols
def num_next(unit, L, its, prompt="What number comes next?"):
    seq = build(unit, L)
    k = len(unit)
    ans = unit[L % k]
    vals = [int(t.split(":")[1]) for t in unit]
    last = int(seq[-1].split(":")[1])
    d = vals[1] - vals[0]
    step = d if d and all(b - a == d for a, b in zip(vals, vals[1:])) else 1
    on = last + step                         # the mistake: keep counting instead of repeating
    cands = ["n:%d" % on, seq[L - 2], seq[L - 1], unit[(L + 1) % k], unit[0]]
    r = L % k
    e = ("The numbers repeat. The repeating unit is <i>%s</i>. %s Next is <b>%s</b>."
         % (names(unit), "The last unit is finished, so start again." if r == 0 else
            "The last unit so far is %s." % names(unit[:r]), name(ans)))
    if on != int(name(ans)) and on > 0:
        e += " %d is counting %s, not repeating." % (on, "back" if step < 0 else "on")
    q = fig(row_svg(seq + ["?"], "a number pattern")) + prompt
    its.append(mcq(q, name(ans), [name(t) for t in cands if t != ans] + [str(max(vals) + step), str(last + 2)], e))


def sym_next(unit, L, pool, its, prompt):
    seq = build(unit, L)
    k = len(unit)
    ans = unit[L % k]
    cands = [seq[L - 2], seq[L - 1], unit[0], unit[(L + 1) % k]] + [t for t in pool if t not in unit]
    r = L % k
    e = ("The repeating unit is <i>%s</i>. %s Next is <b>%s</b>."
         % (names(unit), "The last unit is finished, so start again." if r == 0 else
            "The last unit so far is %s." % names(unit[:r]), name(ans)))
    q = fig(row_svg(seq + ["?"], "a symbol pattern")) + prompt
    its.append(mcq(q, name(ans), [name(t) for t in cands if t != ans], e))


def set_numbers(rnd):
    its = []
    N = lambda xs: ["n:%d" % x for x in xs]
    num_next(N([1, 2]), 8, its)
    num_next(N([1, 2, 3]), 9, its)
    num_next(N([5, 5, 8]), 8, its)
    num_next(N([2, 7, 7]), 6, its)
    num_next(N([4, 3, 2]), 9, its)
    num_next(N([10, 20, 30]), 6, its)
    # number gaps
    for unit, L, p in [([3, 6], 8, 5), ([4, 4, 7], 9, 4), ([9, 8, 7], 9, 5), ([2, 4, 6, 8], 8, 6)]:
        seq = build(N(unit), L)
        ans = seq[p]
        a = int(ans.split(":")[1])
        shown = seq[:p] + ["?"] + seq[p + 1:]
        left, right = int(seq[p - 1].split(":")[1]), int(seq[p + 1].split(":")[1])
        cands = [left, right, a + 1, a - 1] + unit
        e = ("The repeating unit is <i>%s</i>. Say it along the row: the gap gets <b>%d</b>."
             % (", ".join(map(str, unit)), a))
        if unit == [2, 4, 6, 8]:
            e += " After 8 the unit starts again at 2."
        q = fig(row_svg(shown, "a number pattern")) + "What number is missing?"
        its.append(mcq(q, a, [c for c in cands if c != a], e))
    # number unit in words
    for unit, n in [([1, 2, 3], 9), ([6, 6, 1], 9)]:
        seq = build(N(unit), n)
        right = ", ".join(map(str, unit))
        wrong = [", ".join(map(str, unit[:-1])), ", ".join(map(str, unit + [unit[0]])), ", ".join(map(str, unit[::-1]))]
        if unit == [6, 6, 1]:
            wrong[2] = "6, 1"
        q = fig(row_svg(seq, "a number pattern")) + "What is the repeating unit?"
        e = "%s repeats, then starts again. The repeating unit is <b>%s</b>." % (right, right)
        its.append(mcq(q, right, wrong, e))
    # next two numbers
    seq = build(N([1, 2, 3]), 8)
    q = fig(row_svg(seq + ["?", "?"], "a number pattern")) + "What are the next two numbers?"
    its.append(mcq(q, "3, 1", ["4, 5", "1, 2", "2, 3"],
                   "The repeating unit is <i>1, 2, 3</i>. After 1, 2 comes 3, then start again with 1. Answer: <b>3, 1</b>. "
                   "4, 5 is counting on, not repeating."))
    # letters
    L_ = lambda xs: ["l:" + x for x in xs]
    sym_next(L_(["A", "B", "B"]), 7, L_(["C", "D"]), its, "What letter comes next?")
    sym_next(L_(["X", "O"]), 7, L_(["Y", "Z"]), its, "What comes next?")
    sym_next(L_(["X", "X", "O"]), 8, L_(["Y", "Z"]), its, "What comes next?")
    # arrows
    A_ = lambda xs: ["a:" + x for x in xs]
    pool = A_(["up", "down", "left", "right"])
    sym_next(A_(["up", "down"]), 7, pool, its, "Which arrow comes next?")
    sym_next(A_(["left", "right", "right"]), 7, pool, its, "Which arrow comes next?")
    sym_next(A_(["up", "right", "down", "left"]), 6, pool, its, "Which arrow comes next?")
    # symbols + and −
    S_ = lambda xs: ["l:" + x for x in xs]
    sym_next(S_(["+", "−", "−"]), 8, S_(["=", "○"]), its, "Which symbol comes next?")
    assert len(its) == 20, len(its)
    return {"title": "Number and symbol patterns", "items": its}


# ============================================================ set 5: make and use patterns (stories)
def set_stories(rnd, P):
    its = []
    # 1-5: which row is a repeating pattern?
    for mode, st, prompt in [
            ("bead", "ABB", "%s makes 4 bead strings. Which string has a repeating pattern?"),
            ("flag", "ABC", "%s hangs flags for the athletics carnival. Which line of flags is a repeating pattern?"),
            ("obj", "AB", "%s lines up shells and starfish at the beach. Which row is a repeating pattern?"),
            ("shape", "AAB", "%s draws 4 rows of shapes. Which row is a repeating pattern?"),
            ("num", "ABC", "%s writes 4 rows of numbers. Which row is a repeating pattern?")]:
        nm = P.next()[0]
        if mode == "num":
            pool = ["n:%d" % x for x in (1, 2, 3, 4)]
            unit = pool[:3]
        elif mode == "obj":
            pool = ["o:shell", "o:starfish"]
            unit = pool[:] if rnd.random() < 0.5 else pool[::-1]
        else:
            pool = pool_for(mode, rnd)
            unit = from_structure(st, pool, rnd)
        n = 9
        right = build(unit, n)
        assert period(right) == len(unit)
        wrong = broken_rows(unit, pool, n, rnd)
        for w in wrong:
            assert period(w) is None, w
        e = ("Row {L} repeats <i>%s</i> again and again. In the other rows the order changes, so they are not "
             "repeating patterns." % names(unit))
        its.append(abcd_item(prompt % nm, rows_svg, right, wrong, e))
    # 6-7: which one is wrong?
    for mode, st in [("bead", "AAB"), ("shape", "ABC")]:
        nm, he, his = P.next()
        pool = pool_for(mode, rnd)
        unit = from_structure(st, pool, rnd)
        n = 9
        seq = build(unit, n)
        for _ in range(100):
            i = rnd.randrange(len(unit), n - 1)
            t = rnd.choice([x for x in unit if x != seq[i]])
            bad = seq[:i] + [t] + seq[i + 1:]
            fixes = [j for j in range(n) for v in pool if v != bad[j]
                     and period(bad[:j] + [v] + bad[j + 1:]) is not None]
            if period(bad) is None and set(fixes) == {i}:
                break
        else:
            raise AssertionError("no unique mistake")
        word = "bead" if mode == "bead" else "shape"
        q = (fig(numbered_svg(bad, "a pattern with one mistake")) +
             "%s made a repeating pattern, but %s made one mistake. Which %s is wrong?" % (nm, he, word))
        e = ("The repeating unit is %s. Say it along the row. %s %d should be %s, so <b>%d</b> is wrong."
             % (say_unit(unit, "colour" if mode == "bead" else "shape"), word.capitalize(), i + 1,
                name(seq[i], "colour" if mode == "bead" else "shape"), i + 1))
        its.append(mcq(q, i + 1, [x for x in [i, i + 2, i + 1 + len(unit), i + 1 - len(unit), n, 1] if 1 <= x <= n], e))
    # 8-10: how many in all?
    nm, he, his = P.next()
    unit = ["b:red", "b:blue", "b:blue"]
    q = (fig(row_svg(unit, "one repeating unit: red, blue, blue")) +
         "%s threads this repeating unit 3 times. How many beads does %s use?" % (nm, he))
    its.append(mcq(q, 9, [6, 3, 12, 8],
                   "Each unit has 3 beads. 3, 6, 9. %s uses <b>9</b> beads. 6 is only 2 beads in each unit." % nm))
    nm, he, his = P.next()
    unit = ["f:red", "f:yellow"]
    q = (fig(row_svg(unit, "one repeating unit: red, yellow")) +
         "%s makes this repeating unit 5 times. How many flags are there?" % nm)
    its.append(mcq(q, 10, [5, 7, 12, 2],
                   "Each unit has 2 flags. 2, 4, 6, 8, 10. There are <b>10</b> flags. 5 counts the units, not the flags."))
    nm, he, his = P.next()
    col = rnd.choice(["blue", "green"])
    unit = ["c:%s:circle" % col, "c:%s:circle" % col, "c:%s:square" % col, "c:%s:square" % col]
    q = (fig(row_svg(unit, "one repeating unit: circle, circle, square, square")) +
         "%s draws this repeating unit 2 times. How many shapes does %s draw?" % (nm, he))
    its.append(mcq(q, 8, [4, 6, 2, 10],
                   "Each unit has 4 shapes. 4 + 4 = <b>8</b>. 4 is only one unit. 2 counts the units."))
    # 11: how many blue beads?
    nm, he, his = P.next()
    seq = build(["b:red", "b:blue"], 6)
    q = (fig(row_svg(seq, "beads: red, blue, red, blue, red, blue")) +
         "%s keeps going with this pattern. %s uses 8 red beads in all. How many blue beads does %s use?"
         % (nm, he.capitalize(), he))
    its.append(mcq(q, 8, [7, 16, 9, 4],
                   "The unit is red, blue. Each red bead has one blue bead after it. 8 red beads, so <b>8</b> blue beads."))
    # 12-18: next / missing in a story
    nm, he, his = P.next()
    pool = pool_for("bead", rnd)
    next_item(from_structure("ABB", pool, rnd), "bead", pool, 7, its, "What colour is the next bead?",
              "%s threads beads. " % nm)
    nm, he, his = P.next()
    pool = pool_for("flag", rnd)
    next_item(from_structure("ABC", pool, rnd), "flag", pool, 7, its, "What colour is the next flag?",
              "%s hangs flags for the swimming carnival. " % nm)
    nm, he, his = P.next()
    gap_item(["o:shell", "o:shell", "o:starfish"], "obj", ["o:shell", "o:starfish", "o:leaf", "o:apple"], 9, 4, its,
             "%s lines up shells and starfish at the beach. " % nm)
    nm, he, his = P.next()
    W_ = ["w:clap", "w:stamp", "w:stamp"]
    seq = build(W_, 7)
    q = (fig(row_svg(seq + ["?"], "clap, stamp, stamp, clap, stamp, stamp, clap")) +
         "%s claps and stamps in a pattern. What does %s do next?" % (nm, he))
    its.append(mcq(q, "stamp", ["clap", "jump", "click"],
                   "The repeating unit is <i>clap, stamp, stamp</i>. The last unit so far is clap. Next is <b>stamp</b>."))
    nm, he, his = P.next()
    pool = pool_for("both", rnd)
    next_two(from_structure("ABB", pool, rnd), "both", pool, 7, its, "%s makes a path with tiles. " % nm)
    nm, he, his = P.next()
    pool = ["a:up", "a:down", "a:left", "a:right"]
    sym_next(["a:up", "a:up", "a:down"], 8, pool, its,
             "%s does a dance. The arrows show %s moves. Which arrow comes next?" % (nm, his))
    nm, he, his = P.next()
    pool = pool_for("bead", rnd)
    two_gaps(from_structure("AB", pool, rnd), "bead", pool, 9, 3, 6, its, "%s threads a bead string. " % nm)
    # 19: make a pattern with a given unit
    nm, he, his = P.next()
    col = rnd.choice(["red", "blue"])
    U = ["c:%s:circle" % col, "c:%s:star" % col, "c:%s:star" % col]
    right = build(U, 9)
    wrong = [build([U[0], U[1]], 9), build([U[0], U[0], U[1]], 9),
             right[:3] + [U[1]] + right[4:]]
    for w in wrong:
        assert w != right
    assert period(wrong[2]) is None
    e = ("Row {L} repeats circle, star, star. Circle, star is a unit that is too short. "
         "Circle, circle, star is the wrong unit. One row breaks the pattern.")
    its.append(abcd_item("%s makes a pattern with the repeating unit circle, star, star. Which row did %s make?"
                         % (nm, he), rows_svg, right, wrong, e))
    # 20: how many times
    nm, he, his = P.next()
    seq = build(["b:red", "b:blue"], 6)
    q = (fig(row_svg(seq, "beads: red, blue, red, blue, red, blue")) +
         "%s threads red, blue, red, blue, red, blue. How many times does red, blue repeat?" % nm)
    its.append(mcq(q, 3, [6, 2, 4], "Put a loop around each red, blue: there are <b>3</b> units. 6 counts the beads."))
    assert len(its) == 20, len(its)
    return {"title": "Make and use patterns (stories)", "items": its}


# ============================================================ balance (and build A-D pictures)
def balance(sets, rnd):
    for s in sets:
        targets = [0, 1, 2, 3] * 5
        rnd.shuffle(targets)
        for it, t in zip(s["items"], targets):
            if "_abcd" in it:
                prompt, builder, right, wrong = it.pop("_abcd")
                wrong = list(wrong)
                rnd.shuffle(wrong)
                panels = wrong[:t] + [right] + wrong[t:]
                if builder is units_svg:
                    svg = units_svg(it.pop("_top"), panels)
                else:
                    svg = builder(panels)
                it["q"] = fig(svg) + prompt
                it["a"] = t
                it["e"] = it["e"].replace("{L}", "ABCD"[t])
                continue
            c = it["c"]
            right = c[it["a"]]
            wrong = [x for i, x in enumerate(c) if i != it["a"]]
            rnd.shuffle(wrong)
            it["c"] = wrong[:t] + [right] + wrong[t:]
            it["a"] = t


# ============================================================ lesson
def body_html():
    ab = build(["c:red:circle", "c:blue:circle"], 6)
    abb = build(["c:green:triangle", "c:green:square", "c:green:square"], 7)
    nums = build(["n:1", "n:2", "n:3"], 7)
    return (
        "<h2>What is a repeating pattern?</h2>"
        "<p>A repeating pattern has a part that comes again and again. "
        "That part is called the <b>repeating unit</b>. "
        "Find the unit. Then say it again and again to keep the pattern going.</p>"
        + "<figure class='sn-fig'>" + row_svg(ab, "red, blue, red, blue, red, blue")
        + "<figcaption>The repeating unit is red, blue. It repeats 3 times.</figcaption></figure>"
        + table(["Pattern", "Repeating unit", "Things in the unit"], [
            ["red, blue, red, blue", "red, blue", "2"],
            ["circle, star, star, circle, star, star", "circle, star, star", "3"],
            ["1, 2, 3, 1, 2, 3", "1, 2, 3", "3"],
            ["clap, clap, stamp, stamp, clap, clap, stamp, stamp", "clap, clap, stamp, stamp", "4"],
        ])
        + "<h2>What comes next?</h2>"
        "<p>Find where the last unit stops. Then keep saying the unit.</p>"
        + "<figure class='sn-fig'>" + row_svg(abb + ["?"], "triangle, square, square, triangle, square, square, triangle, then a gap")
        + "<figcaption>Triangle, square, square … The last unit so far is triangle. Next is square.</figcaption></figure>"
        + ex("Example", "What comes next? 1, 2, 3, 1, 2, 3, 1, ?",
             "The repeating unit is 1, 2, 3. The last unit so far is 1. Next is 2. This pattern repeats. It does not count on.",
             "2")
        + "<figure class='sn-fig'>" + row_svg(nums + ["?"], "a number pattern 1, 2, 3, 1, 2, 3, 1, then a gap")
        + "<figcaption>Numbers can make a repeating pattern too.</figcaption></figure>"
        + "<h2>What is missing?</h2>"
        "<p>Start at the beginning. Say the unit along the row, one thing at a time. "
        "When you reach the gap, the word you say is the answer.</p>"
        + ex("Example", "Red, red, blue, red, ?, blue. What is missing?",
             "The repeating unit is red, red, blue. Say it: red, red, blue, red, <b>red</b>, blue.", "red")
        + "<h2>Make a pattern</h2>"
        "<p>Choose a unit, such as yellow, blue. Make it again and again: yellow, blue, yellow, blue. "
        "A row is only a repeating pattern if the same unit repeats every time, in the same order.</p>"
        + "<h2>Common mistakes</h2>"
        + table(["Mistake", "What to do instead"], [
            ["Starting the unit again too early: red, blue, blue, red, blue, <b>red</b>",
             "Finish the unit first: red, blue, blue, red, blue, blue"],
            ["Unit too short: calling red, blue, blue a red, blue pattern", "Look for where the whole unit starts again"],
            ["Copying the thing just before the gap", "Say the unit from the start of the row"],
            ["Counting on: 1, 2, 3, 1, 2, 3, then 4", "In a repeating pattern, 1, 2, 3 comes back again"],
        ])
    )


FAQ = [
    {"q": "What is a repeating unit in Year 1 maths?",
     "a": "The repeating unit is the part of a pattern that repeats again and again. In red, blue, blue, red, blue, blue, the repeating unit is red, blue, blue. Year 1 students identify the repeating unit to continue and create patterns (AC9M1A02)."},
    {"q": "What kinds of repeating patterns do Year 1 students learn?",
     "a": "They work with patterns of colours, shapes, objects, numbers and symbols, such as AB (red, blue), ABB (circle, star, star), AAB and ABC patterns. They continue a pattern, find a missing part and make their own."},
    {"q": "How can I help my child with patterns at home?",
     "a": "Make patterns with beads, blocks, pegs or leaves, or with actions such as clap, stamp, stamp. Ask your child to say the pattern aloud, point to the repeating unit and tell you what comes next."},
    {"q": "Why are repeating patterns part of algebra?",
     "a": "Finding a repeating unit means noticing a rule and using it to predict what comes next. This is the start of algebraic thinking in the Australian Curriculum, and it leads to skip counting and number patterns."},
]


def gen():
    rnd = random.Random(1807)
    P = People(rnd)
    sets = [set_next(rnd), set_unit(rnd), set_gaps(rnd), set_numbers(rnd), set_stories(rnd, P)]
    balance(sets, rnd)
    seen = set()
    for s in sets:
        assert len(s["items"]) == 20, (s["title"], len(s["items"]))
        assert sorted(it["a"] for it in s["items"]) == sorted([0, 1, 2, 3] * 5), s["title"]
        for it in s["items"]:
            assert len(set(it["c"])) == 4, it
            assert "_abcd" not in it and "_top" not in it and "{" not in it["e"]
            assert it["q"].count("<svg") == 1, it["q"]
            assert it["q"] not in seen, it["q"]
            seen.add(it["q"])
            for c in it["c"]:
                for tok in re.findall(r"\d+", c):
                    assert 0 < int(tok) <= 120, c
    u = {
        "country": "au", "subject": "maths", "grade": "year-1", "slug": "repeating-patterns", "sort": 7,
        "updated": UPDATED, "pdf_url": "",
        "title": "Repeating Patterns",
        "seo_title": "Year 1 Repeating Patterns Worksheets: Shapes, Colours and Numbers (Free, Australian Curriculum)",
        "short_title": "Repeating patterns",
        "domain": "Algebra",
        "standard_code": "AC9M1A02",
        "standard_url": "https://v9.australiancurriculum.edu.au/f-10-curriculum/learning-areas/mathematics",
        "standard_text": "Recognise, continue and create repeating patterns with numbers, symbols, shapes and objects, identifying the repeating unit",
        "meta_desc": "Free Year 1 maths worksheets on repeating patterns: continue AB, ABB, AAB and ABC patterns, find the repeating unit, fill in the missing part, and make patterns with shapes, colours, objects, numbers and symbols. 100 picture questions with an answer key, following the Australian Curriculum.",
        "key_big": "Find the part that repeats. Then say it again and again.",
        "key_sub": "That part is the repeating unit. Finish each unit before you start it again, and check the whole unit repeats in the same order.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }
    return u


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
