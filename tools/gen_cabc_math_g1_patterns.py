# -*- coding: utf-8 -*-
"""
British Columbia Grade 1 Math: Repeating patterns (BC Mathematics Curriculum, Patterning)
  python3 tools/gen_cabc_math_g1_patterns.py
Repeating patterns with multiple elements and attributes: find the core (AB, AAB, ABC), what comes
next, patterns where two attributes change (colour and shape), what is missing, and making the same
pattern with letters (and with actions or other things).
Every pattern is a list of tokens built from its core, so every answer and every picture is
computed from that list and checked in code.
Wrong answers come from real mistakes: the wrong core (too short, one too long, starting in the
wrong place), copying one element (the last thing shown, or only the colour / only the shape),
going one step too far, counting on instead of repeating, and swapping the letters.
HTML attributes use single quotes (no backslashes in the JSON).
"""
import json, math, os, random, re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "ca-bc", "math", "grade-1")
UPDATED = "2026-11-02"
GREEN = "#006633"
FILL = "#e8f3ec"
RED_INK = "#c0392b"
GREY = "#9a9a9a"
INK = "#2b2b2b"
FONT = "Arial, Helvetica, sans-serif"
COLOURS = {"red": "#d64535", "yellow": "#f4c430", "blue": "#2e6da4", "green": "#3a9a4a"}
PLAIN = ["red", "yellow", "blue"]                  # colour-only patterns (stay different in grey print)
SHAPES = ["circle", "square", "triangle", "star"]
OBJECTS = ["leaf", "apple", "fish", "mitt"]
SOUNDS = ["drum", "bell", "shaker", "whistle"]
ACTIONS = ["clap", "stomp", "snap", "jump"]
GIRLS = ["Olivia", "Ava", "Chloe", "Simran", "Jasleen", "Mei", "Hana", "Sofia", "Emma", "Leah", "Zara", "Nadia"]
BOYS = ["Liam", "Ethan", "Noah", "Arjun", "Harjot", "Wei", "Mateo", "Lucas", "Kai", "Owen", "Ryan"]


# ------------------------------------------------------------ tokens
# "c:red:circle" coloured shape ("c:red:circle:s" a small one), "o:apple" object, "s:drum" sound
# picture, "w:clap" action word, "n:3" number, "l:A" letter
def name(tok, mode=None):
    p = tok.split(":")
    if p[0] == "c":
        if mode == "size":
            return "small" if len(p) == 4 else "big"
        return {"colour": p[1], "shape": p[2]}.get(mode, p[1] + " " + p[2])
    return p[1]


def names(toks, mode=None):
    return ", ".join(name(t, mode) for t in toks)


def build(unit, n):
    return [unit[i % len(unit)] for i in range(n)]


def is_rotation(a, b):
    return len(a) == len(b) and any(a[i:] + a[:i] == b for i in range(len(a)))


def from_structure(struct, pool, rnd):
    """'AAB' + pool -> core with different tokens for different letters."""
    letters = sorted(set(struct))
    pick = rnd.sample(pool, len(letters))
    m = dict(zip(letters, pick))
    return [m[ch] for ch in struct]


def pool_for(mode, rnd):
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
    if mode == "sound":
        return ["s:" + o for o in SOUNDS]
    if mode == "word":
        return ["w:" + o for o in ACTIONS]
    if mode == "letter":
        return ["l:" + x for x in "XOTS"]
    raise ValueError(mode)


def outsiders(unit, mode, pool):
    """Things not in the pattern (a new colour or a new shape), most likely first."""
    out = [t for t in pool if t not in unit]
    if mode == "colour":
        sh = unit[0].split(":")[2]
        out.append("c:green:" + sh)
    if mode == "both":
        for t in unit:
            c, s = t.split(":")[1:]
            for t2 in unit:
                c2, s2 = t2.split(":")[1:]
                if c != c2:
                    out.append("c:%s:%s" % (c, s2))
    seen, res = set(unit), []
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


def abcd_item(prompt, builder, right, wrong, e, top=None):
    assert len(wrong) == 3 and right not in wrong and len({repr(w) for w in wrong}) == 3
    it = {"q": "", "c": ["A", "B", "C", "D"], "a": 0, "e": e, "_abcd": (prompt, builder, right, wrong)}
    if top is not None:
        it["_top"] = top
    return it


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


def svg_wrap(w, h, body, label, large=None):
    if large is None:
        large = w > 170
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
    if kind == "leaf":
        return ("<path d='M %.1f %.1f Q %.1f %.1f %.1f %.1f Q %.1f %.1f %.1f %.1f Z' fill='#e08a2c' stroke='#8a4b12' stroke-width='1.5'/>"
                "<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='#8a4b12' stroke-width='1.2'/>"
                % (cx - 14 * s, cy + 12 * s, cx - 14 * s, cy - 14 * s, cx + 14 * s, cy - 14 * s,
                   cx + 14 * s, cy + 12 * s, cx - 14 * s, cy + 12 * s,
                   cx - 14 * s, cy + 12 * s, cx + 9 * s, cy - 9 * s))
    if kind == "apple":
        return ("<circle cx='%.1f' cy='%.1f' r='%.1f' fill='#d64535' stroke='#7a1f16' stroke-width='1.5'/>"
                "<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='#6b4a2a' stroke-width='2.2'/>"
                "<ellipse cx='%.1f' cy='%.1f' rx='%.1f' ry='%.1f' fill='#3a9a4a'/>"
                % (cx, cy + 3 * s, 13 * s, cx, cy - 9 * s, cx + 2 * s, cy - 16 * s,
                   cx + 7 * s, cy - 13 * s, 5 * s, 2.5 * s))
    if kind == "mitt":
        return ("<rect x='%.1f' y='%.1f' width='%.1f' height='%.1f' rx='%.1f' fill='#2e6da4' stroke='%s' stroke-width='1.5'/>"
                "<ellipse cx='%.1f' cy='%.1f' rx='%.1f' ry='%.1f' fill='#2e6da4' stroke='%s' stroke-width='1.5' "
                "transform='rotate(-30 %.1f %.1f)'/>"
                "<rect x='%.1f' y='%.1f' width='%.1f' height='%.1f' rx='%.1f' fill='#ffffff' stroke='%s' stroke-width='1.5'/>"
                % (cx - 9 * s, cy - 16 * s, 18 * s, 26 * s, 9 * s, INK,
                   cx + 10 * s, cy - 1 * s, 4.5 * s, 8 * s, INK, cx + 10 * s, cy - 1 * s,
                   cx - 10 * s, cy + 8 * s, 20 * s, 8 * s, 2 * s, INK))
    if kind == "fish":                                  # a salmon swimming left
        return ("<polygon points='%.1f,%.1f %.1f,%.1f %.1f,%.1f' fill='#e07a5f' stroke='#7a2e1f' stroke-width='1.5' "
                "stroke-linejoin='round'/>"
                "<ellipse cx='%.1f' cy='%.1f' rx='%.1f' ry='%.1f' fill='#e07a5f' stroke='#7a2e1f' stroke-width='1.5'/>"
                "<circle cx='%.1f' cy='%.1f' r='%.1f' fill='%s'/>"
                % (cx + 8 * s, cy, cx + 18 * s, cy - 9 * s, cx + 18 * s, cy + 9 * s,
                   cx - 3 * s, cy, 13 * s, 8 * s,
                   cx - 10 * s, cy - 2 * s, 1.9 * s, INK))
    raise ValueError(kind)


def sound(kind, cx, cy, c):
    s = c / 40.0
    if kind == "drum":
        return ("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='#6b4a2a' stroke-width='2.4'/>"
                "<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='#6b4a2a' stroke-width='2.4'/>"
                "<rect x='%.1f' y='%.1f' width='%.1f' height='%.1f' fill='#d64535' stroke='%s' stroke-width='1.5'/>"
                "<ellipse cx='%.1f' cy='%.1f' rx='%.1f' ry='%.1f' fill='#f5e6c8' stroke='%s' stroke-width='1.5'/>"
                "<ellipse cx='%.1f' cy='%.1f' rx='%.1f' ry='%.1f' fill='none' stroke='%s' stroke-width='1.5'/>"
                % (cx - 12 * s, cy - 18 * s, cx - 3 * s, cy - 6 * s, cx + 12 * s, cy - 18 * s, cx + 3 * s, cy - 6 * s,
                   cx - 14 * s, cy - 5 * s, 28 * s, 18 * s, INK,
                   cx, cy - 5 * s, 14 * s, 4 * s, INK, cx, cy + 13 * s, 14 * s, 4 * s, INK))
    if kind == "bell":
        return ("<circle cx='%.1f' cy='%.1f' r='%.1f' fill='none' stroke='#8a6a1a' stroke-width='2'/>"
                "<path d='M %.1f %.1f Q %.1f %.1f %.1f %.1f Q %.1f %.1f %.1f %.1f Z' fill='%s' stroke='#8a6a1a' stroke-width='1.5'/>"
                "<circle cx='%.1f' cy='%.1f' r='%.1f' fill='#8a6a1a'/>"
                % (cx, cy - 15 * s, 3 * s,
                   cx - 14 * s, cy + 10 * s, cx - 13 * s, cy - 14 * s, cx, cy - 13 * s,
                   cx + 13 * s, cy - 14 * s, cx + 14 * s, cy + 10 * s, COLOURS["yellow"],
                   cx, cy + 12 * s, 3.5 * s))
    if kind == "shaker":
        return ("<rect x='%.1f' y='%.1f' width='%.1f' height='%.1f' rx='%.1f' fill='#6b4a2a'/>"
                "<ellipse cx='%.1f' cy='%.1f' rx='%.1f' ry='%.1f' fill='#8e5bb5' stroke='%s' stroke-width='1.5'/>"
                "<path d='M %.1f %.1f Q %.1f %.1f %.1f %.1f M %.1f %.1f Q %.1f %.1f %.1f %.1f' fill='none' stroke='#f4c430' stroke-width='2.2'/>"
                % (cx - 2.5 * s, cy + 2 * s, 5 * s, 16 * s, 2 * s,
                   cx, cy - 6 * s, 10 * s, 11 * s, INK,
                   cx - 9 * s, cy - 10 * s, cx, cy - 6 * s, cx + 9 * s, cy - 10 * s,
                   cx - 9 * s, cy - 3 * s, cx, cy + 1 * s, cx + 9 * s, cy - 3 * s))
    if kind == "whistle":
        return ("<rect x='%.1f' y='%.1f' width='%.1f' height='%.1f' fill='#2e6da4' stroke='%s' stroke-width='1.5'/>"
                "<circle cx='%.1f' cy='%.1f' r='%.1f' fill='#2e6da4' stroke='%s' stroke-width='1.5'/>"
                "<rect x='%.1f' y='%.1f' width='%.1f' height='%.1f' fill='#2e6da4'/>"
                "<circle cx='%.1f' cy='%.1f' r='%.1f' fill='#ffffff'/>"
                % (cx - 16 * s, cy - 6 * s, 20 * s, 8 * s, INK,
                   cx + 6 * s, cy + 4 * s, 10 * s, INK,
                   cx - 2 * s, cy - 5 * s, 6 * s, 6 * s,
                   cx + 6 * s, cy + 4 * s, 3 * s))
    raise ValueError(kind)


def box(x, y, w, h):
    return ("<rect x='%.1f' y='%.1f' width='%.1f' height='%.1f' rx='5' fill='#ffffff' stroke='%s' stroke-width='1.6'/>"
            % (x, y, w, h, GREEN))


def gap_box(x, y, w, h):
    g = ("<rect x='%.1f' y='%.1f' width='%.1f' height='%.1f' rx='5' fill='%s' stroke='%s' stroke-width='1.6' "
         "stroke-dasharray='4 3'/>" % (x + 2, y + 2, w - 4, h - 4, FILL, GREEN))
    return g + text(x + w / 2, y + h / 2 + 7, "?", 20, col=RED_INK)


def cell_w(tokens, c):
    return c + 26 if any(t.startswith("w:") for t in tokens) else c


def token(t, x, y, w, c):
    cx, cy = x + w / 2.0, y + c / 2.0
    p = t.split(":")
    if t == "?":
        return gap_box(x, y, w, c)
    if p[0] == "c":
        if len(p) == 4:                                  # small shape, sitting on the same base line
            return shape(p[2], p[1], cx, cy + 0.18 * c, 0.55 * c)
        return shape(p[2], p[1], cx, cy, c)
    if p[0] == "o":
        return obj(p[1], cx, cy, c)
    if p[0] == "s":
        return sound(p[1], cx, cy, c)
    if p[0] in ("n", "l"):
        return box(x + 2, y + 2, w - 4, c - 4) + text(cx, cy + 0.2 * c, p[1], max(16, int(0.5 * c)))
    if p[0] == "w":
        return box(x + 2, y + 2, w - 4, c - 4) + text(cx, cy + 5, p[1], 15)
    raise ValueError(t)


def row_body(tokens, x0, y0, c=40, gap=4):
    w = cell_w(tokens, c)
    n = len(tokens)
    W = n * w + (n - 1) * gap
    s = [token(t, x0 + i * (w + gap), y0, w, c) for i, t in enumerate(tokens)]
    return "".join(s), W, c


def row_svg(tokens, label="repeating pattern", c=40):
    body, w, h = row_body(tokens, 6, 4, c)
    return svg_wrap(w + 12, h + 8, body, label)


def paired_svg(tokens, letters):
    """Pattern on top, its letters underneath (a '?' letter shows red)."""
    c, gap = 40, 4
    body, w, h = row_body(tokens, 6, 4, c, gap)
    cw = cell_w(tokens, c)
    s = [body]
    for i, L in enumerate(letters):
        x = 6 + i * (cw + gap)
        if L == "?":
            s.append(gap_box(x, 4 + c + 6, cw, 34))
        else:
            s.append(box(x + 2, 4 + c + 8, cw - 4, 30) + text(x + cw / 2.0, 4 + c + 29, L, 18))
    return svg_wrap(w + 12, 4 + c + 6 + 34 + 4, "".join(s), "repeating pattern with letters under it")


def units_svg(pattern, options):
    """The pattern on top, then four core choices A-D (two on each line)."""
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
    W = max(34 + row_body(r, 0, 0, c, gap)[1] + 8 for r in rows)
    for k, r in enumerate(rows):
        y = 6 + k * (c + 10)
        s.append(text(8, y + c / 2.0 + 6, "ABCD"[k], 18, "start"))
        s.append(row_body(r, 34, y, c, gap)[0])
        if k:
            s.append("<line x1='4' y1='%d' x2='%d' y2='%d' stroke='#dddddd' stroke-width='0.8'/>" % (y - 5, W - 4, y - 5))
    return svg_wrap(W, 6 + 4 * (c + 10) - 4, "".join(s), "four rows labelled A to D", large=True)


# ------------------------------------------------------------ question makers
def say(unit, mode):
    return "<i>%s</i>" % names(unit, mode)


def cap(t):
    return t[:1].upper() + t[1:]


def an(word):
    return ("an " if word[0] in "aeiou" else "a ") + word


def next_item(unit, mode, pool, L, its, prompt="What comes next?", pre=""):
    seq = build(unit, L)
    k = len(unit)
    ans = unit[L % k]
    r = L % k
    cands = [seq[L - 1], unit[(L + 1) % k], unit[0]] + [t for t in unit if t != ans] + outsiders(unit, mode, pool)
    if r == 0:
        e = "The core is %s. The last core is done. Start again: <b>%s</b>." % (say(unit, mode), name(ans, mode))
    else:
        e = ("The core is %s. The last core so far is %s. Next is <b>%s</b>."
             % (say(unit, mode), names(unit[:r], mode), name(ans, mode)))
    if name(seq[L - 1], mode) != name(ans, mode):
        e += " %s just copies the last one." % cap(name(seq[L - 1], mode))
    elif name(unit[(L + 1) % k], mode) != name(ans, mode):
        e += " %s is one step too far." % cap(name(unit[(L + 1) % k], mode))
    q = fig(row_svg(seq + ["?"])) + pre + prompt
    its.append(mcq(q, name(ans, mode), [name(t, mode) for t in cands if t != ans], e))


def next_two(unit, mode, pool, L, its, pre=""):
    seq = build(unit, L)
    k = len(unit)
    a, b = unit[L % k], unit[(L + 1) % k]
    c3 = unit[(L + 2) % k]
    ans = names([a, b], mode)
    out = outsiders(unit, mode, pool)
    cands = [names([b, c3], mode), names([b, a], mode), names([seq[L - 1], a], mode), names([a, a], mode),
             names([a, out[0]], mode)]
    e = ("The core is %s. Keep going: next is %s, then %s. Answer: <b>%s</b>."
         % (say(unit, mode), name(a, mode), name(b, mode), ans))
    q = fig(row_svg(seq + ["?", "?"])) + pre + "What are the next two?"
    its.append(mcq(q, ans, cands, e))


def gap_item(unit, mode, pool, L, p, its, pre=""):
    seq = build(unit, L)
    ans = seq[p]
    shown = seq[:p] + ["?"] + seq[p + 1:]
    cands = [seq[p - 1], seq[p + 1]] + [t for t in unit if t != ans] + outsiders(unit, mode, pool)
    e = ("The core is %s. Say it from the start of the row. The gap gets <b>%s</b>."
         % (say(unit, mode), name(ans, mode)))
    if name(seq[p - 1], mode) != name(ans, mode):
        e += " %s just copies the one before the gap." % cap(name(seq[p - 1], mode))
    q = fig(row_svg(shown)) + pre + "What is missing?"
    its.append(mcq(q, name(ans, mode), [name(t, mode) for t in cands if t != ans], e))


def two_gaps(unit, mode, pool, L, p1, p2, its, pre=""):
    seq = build(unit, L)
    a, b = seq[p1], seq[p2]
    shown = [("?" if i in (p1, p2) else t) for i, t in enumerate(seq)]
    ans = names([a, b], mode)
    out = outsiders(unit, mode, pool)
    cands = [names([b, a], mode), names([seq[p1 - 1], seq[p2 - 1]], mode), names([seq[p1 + 1], seq[p2 + 1]], mode),
             names([a, out[0]], mode), names([out[0], b], mode), names([a, a], mode), names([b, b], mode)]
    e = ("The core is %s. Say it along the row. The first gap is %s. The second gap is %s. "
         "Answer: <b>%s</b>." % (say(unit, mode), name(a, mode), name(b, mode), ans))
    q = fig(row_svg(shown)) + pre + "What goes in the two gaps? Go from left to right."
    its.append(mcq(q, ans, cands, e))


def wrong_units(unit, rnd, pool):
    """Wrong cores: too short, one too long, starts in the wrong place (or one thing changed)."""
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
    head, rest = res[:3], res[3:]
    rnd.shuffle(rest)
    return head[:2] + [head[2] if rnd.random() < 0.5 else rest[0]]


def struct_of(seq):
    m, out = {}, []
    for t in seq:
        if t not in m:
            m[t] = "ABCD"[len(m)]
        out.append(m[t])
    return out


def spaced(letters):
    return " ".join(letters)


# two attributes
def cs(t):
    return t.split(":")[1], t.split(":")[2]


def mixed_wrong(ans, unit):
    """Right colour + wrong shape, and right shape + wrong colour (copying only one attribute)."""
    col, sh = cs(ans)
    shapes = [cs(t)[1] for t in unit if cs(t)[1] != sh]
    cols = [cs(t)[0] for t in unit if cs(t)[0] != col]
    a = "c:%s:%s" % (col, shapes[0]) if shapes else None
    b = "c:%s:%s" % (cols[0], sh) if cols else None
    return a, b


def both_next(unit, L, its, pre=""):
    seq = build(unit, L)
    k = len(unit)
    ans = unit[L % k]
    a, b = mixed_wrong(ans, unit)
    cands = [x for x in [a, b] if x] + [seq[L - 1], unit[(L + 1) % k]] + [t for t in unit if t != ans]
    e = ("The core is %s. Check the colour and the shape. Next is <b>%s</b>."
         % (say(unit, None), name(ans)))
    if a:
        e += " %s has the right colour but the wrong shape." % cap(an(name(a)))
    elif b:
        e += " %s has the right shape but the wrong colour." % cap(an(name(b)))
    q = fig(row_svg(seq + ["?"])) + pre + "What comes next?"
    its.append(mcq(q, name(ans), [name(t) for t in cands if t != ans], e))


def both_gap(unit, L, p, its, pre=""):
    seq = build(unit, L)
    ans = seq[p]
    a, b = mixed_wrong(ans, unit)
    cands = [x for x in [b, a] if x] + [seq[p - 1], seq[p + 1]] + [t for t in unit if t != ans]
    e = ("The core is %s. Say it from the start of the row. The gap gets <b>%s</b>."
         % (say(unit, None), name(ans)))
    if b:
        e += " %s has the right shape but the wrong colour." % cap(an(name(b)))
    shown = seq[:p] + ["?"] + seq[p + 1:]
    q = fig(row_svg(shown)) + pre + "What is missing?"
    its.append(mcq(q, name(ans), [name(t) for t in cands if t != ans], e))


# ============================================================ set 1: find the core
def set_core(rnd):
    its = []
    for mode, st in [("colour", "AB"), ("shape", "AB"), ("obj", "AB"), ("colour", "AAB"), ("shape", "AAB"),
                     ("sound", "AB"), ("obj", "AAB"), ("shape", "ABC")]:
        pool = pool_for(mode, rnd)
        unit = from_structure(st, pool, rnd)
        k = len(unit)
        pat = build(unit, 3 * k if 3 * k <= 9 else 2 * k)
        wrong = wrong_units(unit, rnd, pool)
        e = ("<i>%s</i> repeats. Then it starts again. So the core is <b>{L}</b>. "
             "Check: the core is not too short and not too long." % cap(names(unit, mode)))
        its.append(abcd_item("What is the core?", units_svg, unit, wrong, e, top=pat))
    # cores of number, letter and action patterns
    for unit, n in [(["n:4", "n:7"], 8), (["n:2", "n:2", "n:5"], 9), (["l:A", "l:B", "l:C"], 9),
                    (["w:clap", "w:clap", "w:stomp"], 6)]:
        seq = build(unit, n)
        right = names(unit)
        wrong = [names(unit[:-1]), names(unit + [unit[0]]), names(unit[1:]), names(unit[::-1])]
        wrong = [w for w in wrong if w != right]
        if len(unit) == 2:
            wrong = [names(unit[:1]), names(unit + [unit[0]]), names(unit[::-1])]
        q = fig(row_svg(seq)) + "What is the core?"
        e = "%s repeats, then starts again. The core is <b>%s</b>." % (cap(right), right)
        if len(unit) == 3:
            e += " %s is too short." % cap(names(unit[:-1]))
        else:
            e += " %s is only one thing. A core has more than one." % names(unit[:1])
        its.append(mcq(q, right, wrong, e))
    # how many in the core
    for mode, st in [("colour", "AB"), ("shape", "ABC"), ("obj", "AAB"), ("colour", "ABC")]:
        pool = pool_for(mode, rnd)
        unit = from_structure(st, pool, rnd)
        k = len(unit)
        n = 3 * k if 3 * k <= 9 else 2 * k
        pat = build(unit, n)
        q = fig(row_svg(pat)) + "How many things are in the core?"
        e = ("The core is %s. It has <b>%d</b> things. Count each one, even if two are the same."
             % (say(unit, mode), k))
        its.append(mcq(q, k, [len(set(unit)), k - 1, k + 1, n, k + 2], e))
    # how many times
    for mode, st, times in [("shape", "AB", 4), ("colour", "ABC", 3), ("obj", "AAB", 3), ("sound", "AB", 5)]:
        pool = pool_for(mode, rnd)
        unit = from_structure(st, pool, rnd)
        k = len(unit)
        q = fig(row_svg(build(unit, k * times))) + "The core is %s. How many times does it repeat?" % names(unit, mode)
        e = ("Draw a loop around each core. There are <b>%d</b> cores. "
             "There are %d things in all, but that is not the answer." % (times, k * times))
        its.append(mcq(q, times, [k * times, times + 1, times - 1, k], e))
    assert len(its) == 20, len(its)
    return {"title": "Find the core (AB, AAB, ABC)", "items": its}


# ============================================================ set 2: what comes next
def num_next(unit, L, its):
    seq = build(unit, L)
    k = len(unit)
    ans = unit[L % k]
    vals = [int(t.split(":")[1]) for t in unit]
    last = int(seq[-1].split(":")[1])
    d = vals[1] - vals[0]
    step = d if d and all(b - a == d for a, b in zip(vals, vals[1:])) else 1
    on = last + step                          # the mistake: count on instead of repeating
    r = L % k
    e = ("The numbers repeat. The core is <i>%s</i>. %s Next is <b>%s</b>."
         % (names(unit), "The last core is done, so start again." if r == 0 else
            "The last core so far is %s." % names(unit[:r]), name(ans)))
    if on != int(name(ans)):
        e += " %d is counting on, not repeating." % on
    q = fig(row_svg(seq + ["?"], "number pattern")) + "What number comes next?"
    its.append(mcq(q, name(ans), [str(on), name(seq[L - 1]), name(unit[(L + 1) % k])] +
                   [name(t) for t in unit] + [str(last + 2)], e))


def set_next(rnd):
    its = []
    specs = [("colour", "AB"), ("shape", "AB"), ("obj", "AB"), ("sound", "AB"), ("word", "AB"),
             ("colour", "AAB"), ("shape", "AAB"), ("obj", "AAB"), ("sound", "AAB"), ("word", "AAB"),
             ("colour", "ABB"), ("shape", "ABC"), ("obj", "ABC"), ("colour", "ABC")]
    used = set()
    for i, (mode, st) in enumerate(specs):
        for _ in range(50):
            pool = pool_for(mode, rnd)
            unit = from_structure(st, pool, rnd)
            if names(unit, mode) not in used:
                break
        used.add(names(unit, mode))
        k = len(unit)
        r = i % k                                  # where the row stops inside the core (varies)
        L = (3 * k if k == 2 else 2 * k) + r
        pre = "Each picture is a sound. " if mode == "sound" and st == "AB" else ""
        next_item(unit, mode, pool, L, its, pre=pre)
    num_next(["n:4", "n:4", "n:1"], 8, its)
    num_next(["n:5", "n:10", "n:15"], 6, its)
    for mode, st, L in [("colour", "AAB", 7), ("shape", "ABC", 8), ("sound", "AB", 7), ("obj", "ABC", 7)]:
        pool = pool_for(mode, rnd)
        next_two(from_structure(st, pool, rnd), mode, pool, L, its)
    assert len(its) == 20, len(its)
    return {"title": "What comes next?", "items": its}


# ============================================================ set 3: two attributes
def set_two(rnd):
    its = []
    # 1-2: core of a colour-and-shape pattern
    for st in ["AB", "AAB"]:
        pool = pool_for("both", rnd)
        unit = from_structure(st, pool, rnd)
        k = len(unit)
        wrong = wrong_units(unit, rnd, pool)
        e = ("<i>%s</i> repeats. Then it starts again. So the core is <b>{L}</b>. "
             "Check the colour and the shape of each one." % cap(names(unit)))
        its.append(abcd_item("What is the core?", units_svg, unit, wrong, e, top=build(unit, 3 * k if k == 2 else 2 * k)))
    # 3-6: what changes?
    ch = ["colour", "shape", "colour and shape", "size"]
    sh = rnd.choice(SHAPES)
    a, b = rnd.sample(PLAIN, 2)
    col = rnd.choice(list(COLOURS))
    s1, s2 = rnd.sample(SHAPES, 2)
    c1, c2 = rnd.sample(PLAIN, 2)
    s3, s4 = rnd.sample(SHAPES, 2)
    c3 = rnd.choice(PLAIN)
    s5 = rnd.choice(["circle", "square", "triangle"])
    for unit, right, e in [
        (["c:%s:%s" % (a, sh), "c:%s:%s" % (b, sh)], "colour",
         "Every one is a %s. Only the colour changes: %s, %s. The answer is <b>colour</b>." % (sh, a, b)),
        (["c:%s:%s" % (col, s1), "c:%s:%s" % (col, s1), "c:%s:%s" % (col, s2)], "shape",
         "Every one is %s. Only the shape changes: %s, %s, %s. The answer is <b>shape</b>." % (col, s1, s1, s2)),
        (["c:%s:%s" % (c1, s3), "c:%s:%s" % (c2, s4)], "colour and shape",
         "The %s is %s. The %s is %s. Both change. The answer is <b>colour and shape</b>." % (s3, c1, s4, c2)),
        (["c:%s:%s" % (c3, s5), "c:%s:%s:s" % (c3, s5)], "size",
         "Every one is a %s %s. Big, small, big, small. The answer is <b>size</b>." % (c3, s5)),
    ]:
        q = fig(row_svg(build(unit, 6))) + "What changes in this pattern?"
        its.append(mcq(q, right, [x for x in ch if x != right], e))
    # 7-12: what comes next (colour and shape change together)
    for i, st in enumerate(["AB", "AAB", "ABB", "ABC", "AB", "ABC"]):
        pool = pool_for("both", rnd)
        unit = from_structure(st, pool, rnd)
        k = len(unit)
        r = (i + 1) % k
        L = (3 * k if k == 2 else 2 * k) + r
        both_next(unit, L, its)
    # 13: next two
    pool = pool_for("both", rnd)
    unit = from_structure("AAB", pool, rnd)
    next_two(unit, "both", pool, 7, its)
    # 14-17: what is missing
    for st, p in [("AB", 3), ("AAB", 4), ("ABB", 5), ("ABC", 4)]:
        pool = pool_for("both", rnd)
        unit = from_structure(st, pool, rnd)
        k = len(unit)
        both_gap(unit, min(3 * k, 9), p, its)
    # 18-20: colour and shape repeat on their own (core of 4)
    x, y = rnd.sample(PLAIN, 2)
    u1, u2 = rnd.sample(SHAPES, 2)
    unit = ["c:%s:%s" % (x, u1), "c:%s:%s" % (y, u1), "c:%s:%s" % (x, u2), "c:%s:%s" % (y, u2)]
    seq = build(unit, 7)
    ans = unit[3]
    e = ("Look at the colours: %s, %s, %s, %s. Look at the shapes: %s, %s, %s, %s. "
         "Next is %s and %s: <b>%s</b>." % (x, y, x, y, u1, u1, u2, u2, y, u2, name(ans)))
    its.append(mcq(fig(row_svg(seq + ["?"])) + "Look at the colour. Look at the shape. What comes next?",
                   name(ans), [name(unit[1]), name(seq[-1]), name(unit[0])], e))
    x, y = rnd.sample(PLAIN, 2)
    u1, u2 = rnd.sample(SHAPES, 2)
    unit = ["c:%s:%s" % (x, u1), "c:%s:%s" % (x, u2), "c:%s:%s" % (y, u1), "c:%s:%s" % (y, u2)]
    seq = build(unit, 6)
    ans = unit[2]
    e = ("Look at the colours: %s, %s, %s, %s. Look at the shapes: %s, %s, %s, %s. "
         "Next is %s and %s: <b>%s</b>." % (x, x, y, y, u1, u2, u1, u2, y, u1, name(ans)))
    its.append(mcq(fig(row_svg(seq + ["?"])) + "Look at the colour. Look at the shape. What comes next?",
                   name(ans), [name(unit[3]), name(unit[0]), name(seq[-1])], e))
    x, y = rnd.sample(PLAIN, 2)
    u1, u2 = rnd.sample(SHAPES, 2)
    unit = ["c:%s:%s" % (x, u1), "c:%s:%s" % (y, u1), "c:%s:%s" % (x, u2), "c:%s:%s" % (y, u2)]
    seq = build(unit, 8)
    p = 6
    ans = seq[p]
    e = ("The colours go %s, %s again and again. The shapes go %s, %s, %s, %s. "
         "The gap is %s and %s: <b>%s</b>." % (x, y, u1, u1, u2, u2, x, u2, name(ans)))
    its.append(mcq(fig(row_svg(seq[:p] + ["?"] + seq[p + 1:])) + "Look at the colour. Look at the shape. What is missing?",
                   name(ans), [name(unit[0]), name(unit[3]), name(unit[1])], e))
    assert len(its) == 20, len(its)
    return {"title": "Two attributes: colour and shape", "items": its}


# ============================================================ set 4: what is missing
def set_missing(rnd):
    its = []
    specs = [("colour", "AB"), ("shape", "AB"), ("obj", "AB"), ("sound", "AB"), ("letter", "AB"),
             ("colour", "AAB"), ("shape", "AAB"), ("obj", "AAB"), ("word", "AAB"), ("letter", "AAB"),
             ("colour", "ABB"), ("colour", "ABC"), ("shape", "ABC"), ("obj", "ABC"), ("sound", "ABC")]
    for mode, st in specs:
        pool = pool_for(mode, rnd)
        unit = from_structure(st, pool, rnd)
        k = len(unit)
        L = 8 if mode == "word" else min(3 * k, 9)
        p = rnd.randint(k, L - 2)            # after one full core, not at the end
        gap_item(unit, mode, pool, L, p, its)
    # a number pattern gap
    seq = build(["n:6", "n:9", "n:9"], 9)
    p = 5
    shown = seq[:p] + ["?"] + seq[p + 1:]
    q = fig(row_svg(shown, "number pattern")) + "What number is missing?"
    its.append(mcq(q, 9, [6, 10, 7, 8],
                   "The core is <i>6, 9, 9</i>. Say it along the row: 6, 9, 9, 6, 9, <b>9</b>. "
                   "10 is counting on, but this pattern repeats."))
    for mode, st in [("colour", "AAB"), ("shape", "ABC"), ("obj", "AAB"), ("sound", "ABC")]:
        pool = pool_for(mode, rnd)
        unit = from_structure(st, pool, rnd)
        p1 = rnd.randint(3, 4)
        p2 = rnd.randint(p1 + 2, 7)
        two_gaps(unit, mode, pool, 9, p1, p2, its)
    assert len(its) == 20, len(its)
    return {"title": "What is missing?", "items": its}


# ============================================================ set 5: same pattern with letters (stories)
CONTEXT = {"colour": "%s makes this pattern with blocks.", "shape": "%s makes this pattern with blocks.",
           "both": "%s makes this pattern with blocks.", "obj": "%s makes a sticker pattern.",
           "sound": "%s plays a music pattern. Each picture is a sound."}


def set_letters(rnd, P):
    its = []
    pat_wrong = {"AB": ["ABB", "AAB", "ABC"], "ABB": ["AB", "AAB", "ABC"], "AAB": ["AB", "ABB", "ABC"],
                 "ABC": ["AB", "ABB", "AAB"]}
    # 1-6: shapes (colours, objects, sounds) to letters
    for mode, st in [("colour", "AB"), ("shape", "AAB"), ("obj", "AAB"), ("colour", "ABC"), ("sound", "AB"),
                     ("both", "AAB")]:
        pool = pool_for(mode, rnd)
        unit = from_structure(st, pool, rnd)
        seq = build(unit, 6)
        right = spaced(struct_of(seq))
        wrong = [spaced(build(list(w), 6)) for w in pat_wrong[st]]
        first, second = name(unit[0], mode), name(next(t for t in unit if t != unit[0]), mode)
        e = ("%s is A. %s is B.%s The core is %s, so it is <b>%s</b>."
             % (cap(first), cap(second),
                " %s is C." % cap(name(unit[2], mode)) if st == "ABC" else "", say(unit, mode), right))
        pre = CONTEXT[mode] % P.next()[0] + " "
        its.append(mcq(fig(row_svg(seq)) + pre + "Which letters show the same pattern?", right, wrong, e))
    # 7-8: what letter goes in the box?
    for mode, st, L, p in [("shape", "ABC", 8, 7), ("obj", "ABC", 8, 6)]:
        pool = pool_for(mode, rnd)
        unit = from_structure(st, pool, rnd)
        seq = build(unit, L)
        lets = struct_of(seq)
        ans = lets[p]
        shown = lets[:p] + ["?"] + lets[p + 1:]
        q = fig(paired_svg(seq, shown)) + "%s writes letters under the pattern. Which letter goes in the box?" % P.next()[0]
        e = ("%s is A, %s is B and %s is C. The box is under %s, so it is <b>%s</b>."
             % (cap(name(unit[0], mode)), name(unit[1], mode), name(unit[2], mode), an(name(seq[p], mode)), ans))
        its.append(mcq(q, ans, [x for x in ["A", "B", "C", "D"] if x != ans], e))
    # 9-12: shapes to actions (gym class)
    for mode, st, acts in [("colour", "AB", ("clap", "stomp")), ("shape", "AAB", ("clap", "stomp")),
                           ("shape", "ABB", ("snap", "jump")), ("obj", "AAB", ("jump", "clap"))]:
        pool = pool_for(mode, rnd)
        unit = from_structure(st, pool, rnd)
        seq = build(unit, 6)
        a, b = unit[0], next(t for t in unit if t != unit[0])
        m = {a: acts[0], b: acts[1]}
        swap = {a: acts[1], b: acts[0]}
        right = ", ".join(m[t] for t in unit)
        wrong = [", ".join(swap[t] for t in unit)]
        for w in pat_wrong[st]:
            if "C" not in w:
                wrong.append(", ".join({"A": acts[0], "B": acts[1]}[ch] for ch in w))
        wrong.append(acts[0])                      # copying one element
        q = (fig(row_svg(seq)) + "In gym class, %s for %s. %s for %s. What is the core in actions?"
             % (acts[0], an(name(a, mode)) if mode != "colour" else name(a, mode),
                cap(acts[1]), an(name(b, mode)) if mode != "colour" else name(b, mode)))
        e = ("The core is %s. %s is %s and %s is %s. So the core is <b>%s</b>."
             % (say(unit, mode), cap(name(a, mode)), acts[0], name(b, mode), acts[1], right))
        its.append(mcq(q, right, wrong, e))
    # 13-18: letters to shapes (pick the row)
    for mode, st in [("colour", "AB"), ("shape", "AAB"), ("obj", "AAB"), ("shape", "ABC"), ("both", "AB"),
                     ("colour", "ABB")]:
        pool = pool_for(mode, rnd)
        unit = from_structure(st, pool, rnd)
        right = build(unit, 6)
        letters = sorted(set(st))
        m = dict(zip(letters, [unit[st.index(ch)] for ch in letters]))
        wrong = [build([m[ch] for ch in w if ch in m], 6) for w in pat_wrong[st] if set(w) <= set(m)]
        if len(wrong) < 3:                     # also: two of each (A A B B)
            wrong.append(build([m["A"], m["A"], m["B"], m["B"]], 6))
        wrong = [w for w in wrong if w != right][:3]
        for w in wrong:
            assert struct_of(w) != struct_of(right), (st, w)
        assert len(wrong) == 3, (st, wrong)
        nm = P.next()[0]
        e = ("%s means %s. Row {L} is %s." % (spaced(st), say(unit, mode), names(right, mode)))
        its.append(abcd_item("%s makes the pattern %s. Which row did %s make?"
                             % (nm, spaced(build(list(st), 6)), "she" if nm in GIRLS else "he"),
                             rows_svg, right, wrong, e))
    # 19-20: same pattern, different things
    for mode1, mode2, st in [("colour", "obj", "AAB"), ("sound", "shape", "ABB")]:
        p1, p2 = pool_for(mode1, rnd), pool_for(mode2, rnd)
        u1, u2 = from_structure(st, p1, rnd), from_structure(st, p2, rnd)
        seq = build(u1, 6)
        right = names(u2, mode2)
        m2 = {ch: u2[st.index(ch)] for ch in set(st)}
        wrong = [names([m2[ch] for ch in w], mode2) for w in pat_wrong[st] if set(w) <= set(m2)]
        wrong.append(names([m2["B" if ch == "A" else "A"] for ch in st], mode2))
        a_old, b_old = u1[st.index("A")], u1[st.index("B")]
        q = (fig(row_svg(seq)) + "Make the same pattern. Use %s for %s. Use %s for %s. Which core is right?"
             % (an(name(m2["A"], mode2)), "the " + name(a_old, mode1) if mode1 == "sound" else name(a_old, mode1),
                an(name(m2["B"], mode2)), "the " + name(b_old, mode1) if mode1 == "sound" else name(b_old, mode1)))
        e = ("The core %s is %s. Swap each thing for its new thing. The new core is <b>%s</b>."
             % (say(u1, mode1), spaced(st), right))
        its.append(mcq(q, right, wrong, e))
    assert len(its) == 20, len(its)
    return {"title": "Make the same pattern with letters", "items": its}


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
                svg = units_svg(it.pop("_top"), panels) if builder is units_svg else builder(panels)
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
    aab = build(["c:green:triangle", "c:green:triangle", "c:green:square"], 7)
    two = build(["c:red:circle", "c:yellow:square", "c:blue:triangle"], 6)
    return (
        "<h2>What is the core?</h2>"
        "<p>A repeating pattern has a part that comes again and again. "
        "That part is the <b>core</b>. Find the core first. "
        "Then say it again and again.</p>"
        + "<figure class='sn-fig'>" + row_svg(ab, "red, blue, red, blue, red, blue")
        + "<figcaption>The core is red, blue. It repeats 3 times.</figcaption></figure>"
        + table(["Pattern", "Core", "Letters"], [
            ["red, blue, red, blue", "red, blue", "A B"],
            ["clap, clap, stomp, clap, clap, stomp", "clap, clap, stomp", "A A B"],
            ["drum, bell, shaker, drum, bell, shaker", "drum, bell, shaker", "A B C"],
        ])
        + "<h2>What comes next?</h2>"
        "<p>Find where the last core stops. Then keep saying the core.</p>"
        + "<figure class='sn-fig'>" + row_svg(aab + ["?"], "triangle, triangle, square, triangle, triangle, square, triangle, then a gap")
        + "<figcaption>Triangle, triangle, square … The last core so far is triangle. Next is triangle.</figcaption></figure>"
        + "<h2>Two things can change</h2>"
        "<p>Look at the colour. Look at the shape. Both must match the core.</p>"
        + "<figure class='sn-fig'>" + row_svg(two + ["?"], "red circle, yellow square, blue triangle, two times, then a gap")
        + "<figcaption>The core is red circle, yellow square, blue triangle. Next is a red circle.</figcaption></figure>"
        + ex("Example", "Red circle, yellow square, blue triangle, red circle, ?",
             "The core has 3 things. After the red circle comes the <b>yellow square</b>. "
             "A yellow circle has the right colour but the wrong shape.", "yellow square")
        + "<h2>What is missing?</h2>"
        + ex("Example", "Apple, apple, fish, apple, ?, fish",
             "The core is apple, apple, fish. Say it from the start: apple, apple, fish, apple, <b>apple</b>, fish.", "apple")
        + "<h2>The same pattern with letters</h2>"
        "<p>Give each new thing a letter. The first thing is A. The next new thing is B. "
        "Then C. Red, red, blue is A A B. Clap, clap, stomp is A A B too. They are the same pattern.</p>"
        + "<h2>Common mistakes</h2>"
        + table(["Mistake", "What to do instead"], [
            ["The wrong core: red, red, blue taken as “red, blue”", "Find where the whole core starts again"],
            ["Copying one thing: writing the last thing again", "Say the core from the start, one thing at a time"],
            ["Looking at only the colour (or only the shape)", "Check the colour and the shape every time"],
            ["Counting on: 1, 2, 3, 1, 2, 3, then 4", "In a repeating pattern, 1, 2, 3 comes back again"],
        ])
    )


FAQ = [
    {"q": "What patterns do Grade 1 students learn in BC math?",
     "a": "In Patterning, BC Grade 1 students work with repeating patterns that have more than one element and attribute, like colour and shape. They find the core, extend the pattern, find what is missing and show the same pattern another way."},
    {"q": "What is the core of a pattern?",
     "a": "The core is the part that repeats. In red, red, blue, red, red, blue, the core is red, red, blue."},
    {"q": "What does AB, AAB or ABC mean in a pattern?",
     "a": "Each letter stands for one thing. Circle, square, circle, square is an AB pattern. Clap, clap, stomp is AAB. Red, yellow, blue is ABC."},
    {"q": "How can I practise patterns with my child at home?",
     "a": "Make patterns with blocks, beads, leaves, rocks or claps and stomps. Ask your child to say the core, what comes next and how to write it with letters."},
]


def gen():
    rnd = random.Random(51806)
    P = People(rnd)
    sets = [set_core(rnd), set_next(rnd), set_two(rnd), set_missing(rnd), set_letters(rnd, P)]
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
                    assert 0 < int(tok) <= 20, c
    u = {
        "country": "ca-bc", "subject": "math", "grade": "grade-1", "slug": "repeating-patterns", "sort": 6,
        "updated": UPDATED, "pdf_url": "",
        "title": "Repeating Patterns: Find the Core, What Comes Next and Colour-and-Shape Patterns",
        "seo_title": "Grade 1 Repeating Patterns Worksheets: AB, AAB, ABC Cores (Free, BC Curriculum Math)",
        "short_title": "Repeating patterns",
        "domain": "Patterning",
        "standard_code": "Grade 1: Patterning",
        "standard_url": "https://curriculum.gov.bc.ca/curriculum/mathematics/1/core",
        "standard_text": "Repeating patterns with multiple elements and attributes",
        "meta_desc": "Free Grade 1 math worksheets on repeating patterns: find the core of AB, AAB and ABC patterns, say what comes next, work with colour-and-shape patterns, find what is missing and show the same pattern with letters. 100 picture questions with an answer key, matched to the BC curriculum.",
        "key_big": "Find the core: the part that repeats. Then say it again and again.",
        "key_sub": "Say the core from the start, one thing at a time. When the colour and the shape both change, check both.",
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
