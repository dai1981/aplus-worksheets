# -*- coding: utf-8 -*-
"""
Singapore Primary 2 Maths: 2D shapes and patterns (MOE 2021 Primary Mathematics Syllabus, Geometry)
  python3 tools/gen_sg_maths_p2_shape_patterns.py
Naming rectangles, squares, triangles, circles, half circles and quarter circles (also when they are
turned), then making and completing repeating patterns by shape, colour, size and orientation:
what comes next, the missing shape in the middle, and patterns where two things change.
Wrong answers come from real mistakes: a wrong core (too short or too long), only looking at the
colour (or only at the shape), repeating the last shape, skipping a shape, thinking a turned shape
has a new name, and getting the turn the wrong way.
Every answer is computed from the pattern in code. HTML attributes use single quotes.
"""
import json, math, os, random, re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "sg", "maths", "primary-2")
UPDATED = "2026-11-03"
GREEN = "#1f4e79"
FILL = "#cfe0f1"
RED = "#c0392b"
INK = "#2b2b2b"
FONT = "Arial, Helvetica, sans-serif"
COLOURS = {"red": "#d64535", "blue": "#3b7dd8", "yellow": "#f2c230", "green": "#4caf50"}
KNAME = {"circle": "circle", "square": "square", "rect": "rectangle", "tri": "triangle",
         "half": "half circle", "quarter": "quarter circle"}
ROTS = {"tri": (0, 90, 180, 270), "half": (0, 90, 180, 270), "quarter": (0, 90, 180, 270),
        "rect": (0, 90), "square": (0, 45), "circle": (0,)}
ROTWORD = {
    "tri": {0: "pointing up", 90: "pointing right", 180: "pointing down", 270: "pointing left"},
    "half": {0: "curved side up", 90: "curved side right", 180: "curved side down", 270: "curved side left"},
    "quarter": {0: "corner at the bottom left", 90: "corner at the top left", 180: "corner at the top right",
                270: "corner at the bottom right"},
    "rect": {0: "lying down", 90: "standing up"},
    "square": {0: "flat", 45: "turned"},
    "circle": {0: ""},
}
ATTRS = ("kind", "col", "size", "rot")
LETTERS = "ABCD"


# ------------------------------------------------------------ helpers
def mcq(q, correct, cands, e):
    """4 choices: correct + the first 3 unique distractors. Positions are set later by balance()."""
    correct = str(correct)
    seen = {correct}
    pick = []
    for c in cands:
        c = str(c)
        if c in seen or not c:
            continue
        seen.add(c)
        pick.append(c)
        if len(pick) == 3:
            break
    assert len(pick) == 3, (q, correct, cands)
    return {"q": q, "c": [correct] + pick, "a": 0, "e": e}


def nums_mcq(q, ans, cands, e):
    ok = [v for v in cands if v != ans and v >= 0]
    assert len(ok) == 3 and len(set(ok)) == 3, (q, ans, cands)
    return mcq(q, str(ans), [str(v) for v in ok], e)


def balance(sets, rnd):
    """Spread the answers 5/5/5/5 in each set. Picture questions (A-D) are built for their slot."""
    for s in sets:
        targets = [0, 1, 2, 3] * 5
        rnd.shuffle(targets)
        for it, t in zip(s["items"], targets):
            if "_build" in it:
                b = it.pop("_build")
                it.update(b(t))
                continue
            c = it["c"]
            right = c[it["a"]]
            wrong = [x for i, x in enumerate(c) if i != it["a"]]
            rnd.shuffle(wrong)
            it["c"] = wrong[:t] + [right] + wrong[t:]
            it["a"] = t


def fig(svg):
    return "<div class='qfig'>" + svg + "</div>"


def svg_wrap(w, h, body, label):
    return ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 %d %d' width='%d' height='%d' "
            "role='img' aria-label='%s'><g font-family='%s'>%s</g></svg>" % (w, h, w, h, label, FONT, body))


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


def mark_large(u, pattern):
    rx = re.compile(r"<svg (?=[^>]*aria-label='" + pattern + ")")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u


def lst(xs):
    return ", ".join(str(x) for x in xs)


def ordn(n):
    suf = "th" if 10 <= n % 100 <= 20 else {1: "st", 2: "nd", 3: "rd"}.get(n % 10, "th")
    return "%d%s" % (n, suf)


# ------------------------------------------------------------ tokens and patterns
def T(kind, col="blue", size="big", rot=0):
    assert kind in KNAME and col in COLOURS and size in ("big", "small") and rot in ROTS[kind], (kind, col, size, rot)
    return (kind, col, size, rot)


def pat(kind, col="blue", size="big", rot=0):
    """A pattern: each attribute has its own core (a list). A plain value means it stays the same."""
    p = {}
    for a, v in zip(ATTRS, (kind, col, size, rot)):
        p[a] = list(v) if isinstance(v, (list, tuple)) else [v]
    return p


def tok(p, i):
    return T(*[p[a][i % len(p[a])] for a in ATTRS])


def toks(p, n):
    return [tok(p, i) for i in range(n)]


def varying(p):
    return [a for a in ATTRS if len(set(p[a])) > 1]


def core_len(p):
    L = 1
    for a in varying(p):
        L = L * len(p[a]) // math.gcd(L, len(p[a]))
    return L


def name(t, show):
    """Words for a token. show: attributes to say, e.g. ('col', 'kind')."""
    kind, col, size, rot = t
    w = []
    if "size" in show:
        w.append(size)
    if "col" in show:
        w.append(col)
    if "rot" in show and kind == "square":
        w.append(ROTWORD["square"][rot])
    if "kind" in show:
        w.append(KNAME[kind])
    s = " ".join(w)
    if "rot" in show and kind not in ("square", "circle"):
        s += (" with its " if kind in ("half", "quarter") else " ") + ROTWORD[kind][rot]
    return s


def attr_word(p, a, v):
    if a == "kind":
        return KNAME[v]
    if a == "rot":
        k = p["kind"][0]
        return ROTWORD[k][v]
    return v


PLURAL = {"kind": "shapes", "col": "colours", "size": "sizes", "rot": "turns"}


def explain(p, show):
    """Describe the core(s) of the pattern."""
    vs = varying(p)
    L = core_len(p)
    if all(len(p[a]) == L for a in vs):
        sh = tuple(show) + tuple(a for a in vs if a not in show)
        if vs == ["col"]:
            return "The colours go <b>%s</b>, then start again." % lst(p["col"])
        return "The core is <b>%s</b>. Then it starts again." % lst(name(tok(p, i), sh) for i in range(L))
    out = []
    for a in vs:
        out.append("The %s go %s." % (PLURAL[a], lst(attr_word(p, a, v) for v in p[a])))
    return " ".join(out)


# ------------------------------------------------------------ drawing
C = 40
SMALL = 0.58


def shape(t, cx, cy, c=C):
    kind, col, size, rot = t
    c = c * (SMALL if size == "small" else 1.0)
    f = COLOURS[col]
    st = "stroke='%s' stroke-width='1.6' stroke-linejoin='round'" % INK
    tr = " transform='rotate(%d %.1f %.1f)'" % (rot, cx, cy) if rot else ""
    if kind == "circle":
        return "<circle cx='%.1f' cy='%.1f' r='%.1f' fill='%s' %s/>" % (cx, cy, 0.42 * c, f, st)
    if kind == "square":
        a = 0.62 * c
        return "<rect x='%.1f' y='%.1f' width='%.1f' height='%.1f' fill='%s' %s%s/>" % (
            cx - a / 2, cy - a / 2, a, a, f, st, tr)
    if kind == "rect":
        w, h = 0.9 * c, 0.46 * c
        return "<rect x='%.1f' y='%.1f' width='%.1f' height='%.1f' fill='%s' %s%s/>" % (
            cx - w / 2, cy - h / 2, w, h, f, st, tr)
    if kind == "tri":
        h, b = 0.8 * c, 0.84 * c
        return ("<polygon points='%.1f,%.1f %.1f,%.1f %.1f,%.1f' fill='%s' %s%s/>"
                % (cx, cy - h / 2, cx + b / 2, cy + h / 2, cx - b / 2, cy + h / 2, f, st, tr))
    if kind == "half":
        r = 0.46 * c
        return ("<path d='M %.1f %.1f A %.1f %.1f 0 0 1 %.1f %.1f Z' fill='%s' %s%s/>"
                % (cx - r, cy + r / 2, r, r, cx + r, cy + r / 2, f, st, tr))
    if kind == "quarter":
        r = 0.8 * c
        x0, y0 = cx - r / 2, cy + r / 2
        return ("<path d='M %.1f %.1f L %.1f %.1f A %.1f %.1f 0 0 1 %.1f %.1f Z' fill='%s' %s%s/>"
                % (x0, y0, x0, y0 - r, r, r, x0 + r, y0, f, st, tr))
    raise ValueError(kind)


def qbox(x, y, w, h):
    return ("<rect x='%.1f' y='%.1f' width='%.1f' height='%.1f' rx='5' fill='%s' stroke='%s' stroke-width='1.6' "
            "stroke-dasharray='4 3'/>" % (x + 1, y + 1, w - 2, h - 2, FILL, GREEN)
            + text(x + w / 2, y + h / 2 + 7, "?", 20, col=RED))


GAP, M = 4, 6


def row_parts(tokens, y0, numbered=False):
    """Returns (svg parts, width, height) of a row of tokens starting at x = M."""
    s = []
    for i, t in enumerate(tokens):
        x = M + i * (C + GAP)
        if t == "?":
            s.append(qbox(x, y0, C, C))
        else:
            s.append(shape(t, x + C / 2, y0 + C / 2))
        if numbered:
            s.append(text(x + C / 2, y0 + C + 17, str(i + 1), 14))
    n = len(tokens)
    return s, n * C + (n - 1) * GAP, C + (21 if numbered else 0)


def row_svg(tokens, numbered=False, label="shape pattern"):
    s, w, h = row_parts(tokens, M, numbered)
    return svg_wrap(int(w + 2 * M), int(h + 2 * M), "".join(s), label)


OB, OG = 50, 22


def opts_svg(tokens, opts, numbered=False):
    """The pattern row on top, then four pictures A, B, C, D in one SVG."""
    s, rw, rh = row_parts(tokens, M, numbered)
    ow = 4 * OB + 3 * OG
    W = max(rw, ow) + 2 * M
    dx = (W - 2 * M - rw) / 2
    if dx:
        s = ["<g transform='translate(%.1f 0)'>%s</g>" % (dx, "".join(s))]
    y = M + rh + 12
    s.append("<line x1='%d' y1='%.1f' x2='%d' y2='%.1f' stroke='%s' stroke-width='1' stroke-dasharray='3 3'/>"
             % (M, y, W - M, y, GREEN))
    y += 10
    x0 = (W - ow) / 2
    for k, t in enumerate(opts):
        x = x0 + k * (OB + OG)
        s.append("<rect x='%.1f' y='%.1f' width='%d' height='%d' rx='6' fill='#ffffff' stroke='%s' stroke-width='1.4'/>"
                 % (x, y, OB, OB, GREEN))
        s.append(shape(t, x + OB / 2, y + OB / 2))
        s.append(text(x + OB / 2, y + OB + 18, LETTERS[k], 16, col=GREEN))
    H = y + OB + 24
    return svg_wrap(int(math.ceil(W)), int(math.ceil(H)), "".join(s), "shape pattern with choices A to D")


def single_svg(t, w=64, h=56):
    return svg_wrap(w, h, shape(t, w / 2, h / 2, 46), "a shape")


def look(t):
    """Key for what a picture looks like."""
    kind, col, size, rot = t
    return (kind, col, size, rot if kind != "circle" else 0)


def pic_q(tokens, lead, ans, wrong, e_tmpl, numbered=False):
    """A-D picture question. e_tmpl contains {L} for the right letter."""
    assert len(wrong) == 3
    looks = [look(ans)] + [look(w) for w in wrong]
    assert len(set(looks)) == 4, (lead, ans, wrong)

    def build(t):
        opts = list(wrong[:t]) + [ans] + list(wrong[t:])
        return {"q": fig(opts_svg(tokens, opts, numbered)) + lead, "c": list(LETTERS), "a": t,
                "e": e_tmpl.format(L=LETTERS[t])}
    return {"_build": build, "q": lead + repr(tokens) + repr(ans), "c": ["A", "B", "C", "D"], "a": 0}


def auto_wrong(p, idx, ans, extra=()):
    """Picture distractors from real mistakes: repeat the last one, skip one, the other turns or sizes."""
    c = list(extra) + [tok(p, idx - 1), tok(p, idx + 1)]
    kind, col, size, rot = ans
    c += [T(kind, col, size, r) for r in ROTS[kind] if r != rot]
    c += [T(kind, col, "small" if size == "big" else "big", rot)]
    c += [T(kind, cc, size, rot) for cc in p["col"] if cc != col]
    near = {"rect": ("square", "tri"), "square": ("rect", "tri")}.get(kind, ("square", "circle"))
    c += [T(k, col, size, 0) for k in near]
    out, seen = [], {look(ans)}
    for t in c:
        if look(t) not in seen:
            seen.add(look(t))
            out.append(t)
    return out[:3]


def text_wrong(p, idx, ans, show, extra=()):
    """Word distractors: repeat the last shape, right colour but wrong shape, right shape but wrong colour, skip one."""
    kind, col, size, rot = ans
    c = [name(t, show) if isinstance(t, tuple) else t for t in extra]
    prev, nxt = tok(p, idx - 1), tok(p, idx + 1)
    c.append(name(prev, show))
    for t in toks(p, core_len(p)):
        if t[1] == col and t[0] != kind:
            c.append(name(t, show))
    for t in toks(p, core_len(p)):
        if t[0] == kind and t[1] != col:
            c.append(name(t, show))
    c.append(name(nxt, show))
    for t in toks(p, core_len(p)):
        if t[2] != size:
            c.append(name(T(kind, col, t[2], rot), show))
    for k in ("square", "circle", "tri", "rect"):
        c.append(name(T(k, col, size, 0), show))
    for cc in ("red", "blue", "yellow", "green"):
        c.append(name(T(kind, cc, size, rot), show))
    return c


# ------------------------------------------------------------ question makers
def next_text(p, shown, show, lead="The pattern repeats. What comes next?", extra=(), tail=""):
    a = tok(p, shown)
    e = explain(p, show) + " So next comes a <b>%s</b>.%s" % (name(a, show), tail)
    return mcq(fig(row_svg(toks(p, shown) + ["?"])) + lead, name(a, show), text_wrong(p, shown, a, show, extra), e)


def miss_text(p, n, i, show, lead="One shape is missing. What is it?", extra=(), tail=""):
    a = tok(p, i)
    row = toks(p, n)
    row[i] = "?"
    e = explain(p, show) + " Say the pattern from the start: %s. The missing shape is a <b>%s</b>.%s" % (
        lst(name(tok(p, k), show) for k in range(i + 1)), name(a, show), tail)
    return mcq(fig(row_svg(row)) + lead, name(a, show), text_wrong(p, i, a, show, extra), e)


def next_pic(p, shown, lead="The pattern repeats. Which shape comes next?", wrong=None, tail="", row=None):
    a = tok(p, shown)
    sh = tuple(varying(p)) + ("kind",)
    w = wrong or auto_wrong(p, shown, a)
    e = explain(p, sh) + " So next comes the %s: <b>{L}</b>.%s" % (name(a, sh), tail)
    return pic_q(row or (toks(p, shown) + ["?"]), lead, a, w, e)


def miss_pic(p, n, i, lead="One shape is missing. Which shape goes in the box?", wrong=None, tail=""):
    a = tok(p, i)
    sh = tuple(varying(p)) + ("kind",)
    row = toks(p, n)
    row[i] = "?"
    w = wrong or auto_wrong(p, i, a)
    e = explain(p, sh) + " Shape %d is the %s: <b>{L}</b>. Check it with the shapes on both sides.%s" % (
        i + 1, name(a, sh), tail)
    return pic_q(row, lead, a, w, e)


# ============================================================ set 1: name the 2D shapes
def set_names():
    def nm(t, ans, cands, e, lead="What is this shape called?"):
        return mcq(fig(single_svg(t)) + lead, ans, cands, e)

    q1 = nm(T("circle", "blue"), "circle", ["half circle", "quarter circle", "square"],
            "It is round all the way. It has no straight sides and no corners. It is a <b>circle</b>.")
    q2 = nm(T("square", "red"), "square", ["rectangle", "triangle", "circle"],
            "It has 4 straight sides that are all the same length and 4 corners. It is a <b>square</b>.")
    q3 = nm(T("tri", "green"), "triangle", ["square", "quarter circle", "rectangle"],
            "It has 3 straight sides and 3 corners. It is a <b>triangle</b>.")
    q4 = nm(T("rect", "yellow"), "rectangle", ["square", "triangle", "half circle"],
            "It has 4 straight sides and 4 corners. Two sides are long and two sides are short. It is a <b>rectangle</b>.")
    q5 = nm(T("half", "blue"), "half circle", ["circle", "quarter circle", "triangle"],
            "It has 1 curved side and 1 straight side. It is half of a circle: a <b>half circle</b>.")
    q6 = nm(T("quarter", "red"), "quarter circle", ["half circle", "triangle", "circle"],
            "It has 2 straight sides and 1 curved side. 4 of them make a circle. It is a <b>quarter circle</b>.")
    q7 = nums_mcq("How many straight sides does a triangle have?", 3, [4, 2, 1],
                  "A triangle has <b>3</b> straight sides and 3 corners.")
    q8 = nm(T("rect", "green", rot=90), "rectangle", ["square", "triangle", "quarter circle"],
            "It has 4 straight sides and 4 corners, with 2 long sides and 2 short sides. It is standing up, "
            "but it is still a <b>rectangle</b>.")
    q9 = nm(T("tri", "yellow", rot=180), "triangle", ["half circle", "square", "quarter circle"],
            "It has 3 straight sides and 3 corners. It points down, but it is still a <b>triangle</b>. "
            "Turning a shape does not change its name.")
    q10 = nums_mcq("How many straight sides does a half circle have?", 1, [2, 0, 3],
                   "A half circle has <b>1</b> straight side and 1 curved side. The curved side is not straight.")
    q11 = nums_mcq("How many corners does a rectangle have?", 4, [3, 2, 5],
                   "A rectangle has 4 sides and <b>4</b> corners, the same as a square.")
    q12 = mcq("Which shape has no straight sides and no corners?", "circle",
              ["half circle", "quarter circle", "square"],
              "A <b>circle</b> is round all the way. A half circle and a quarter circle have straight sides too.")
    q13 = mcq("This shape has 2 straight sides and 1 curved side. What is it?", "quarter circle",
              ["half circle", "triangle", "circle"],
              "A half circle has only 1 straight side. A triangle has no curved side. It is a <b>quarter circle</b>.")
    q14 = nm(T("quarter", "green", rot=180), "quarter circle", ["half circle", "triangle", "circle"],
             "It has 2 straight sides and 1 curved side. It is turned, but it is still a <b>quarter circle</b>.")
    q15 = nm(T("square", "blue", rot=45), "square", ["rectangle", "triangle", "quarter circle"],
             "It has 4 sides of the same length and 4 corners. It is turned, but it is still a <b>square</b>.")

    def which(lead, ans, wrong, e):
        def build(t):
            opts = list(wrong[:t]) + [ans] + list(wrong[t:])
            s, m, bw = [], 6, 64
            for k, o in enumerate(opts):
                x = m + k * (bw + 14)
                s.append("<rect x='%d' y='%d' width='%d' height='%d' rx='6' fill='#ffffff' stroke='%s' stroke-width='1.4'/>"
                         % (x, m, bw, bw, GREEN))
                s.append(shape(o, x + bw / 2, m + bw / 2, 52))
                s.append(text(x + bw / 2, m + bw + 19, LETTERS[k], 16, col=GREEN))
            W = 2 * m + 4 * bw + 3 * 14
            svg = svg_wrap(W, m + bw + 26, "".join(s), "four shapes A to D")
            return {"q": fig(svg) + lead, "c": list(LETTERS), "a": t, "e": e.format(L=LETTERS[t])}
        return {"_build": build, "q": lead, "c": list(LETTERS), "a": 0}

    q16 = which("Which shape is a square?", T("square", "yellow"),
                [T("rect", "yellow"), T("tri", "yellow"), T("quarter", "yellow")],
                "A square has 4 sides of the same length. The rectangle has 2 long sides and 2 short sides. "
                "The square is <b>{L}</b>.")
    q17 = which("Which shape is a quarter circle?", T("quarter", "blue", rot=90),
                [T("half", "blue"), T("circle", "blue"), T("tri", "blue", rot=90)],
                "A quarter circle has 2 straight sides and 1 curved side. It is turned here, but it is still a "
                "quarter circle: <b>{L}</b>.")
    # q18: count the triangles in a picture (one is turned, one is small)
    pics = [T("tri", "red"), T("square", "blue"), T("circle", "yellow"), T("tri", "green", rot=180), T("rect", "red"),
            T("half", "blue"), T("tri", "yellow", rot=90), T("quarter", "green"), T("circle", "red"),
            T("tri", "blue", size="small")]
    ntri = sum(1 for t in pics if t[0] == "tri")
    assert ntri == 4
    s, m = [], 4
    for k, t in enumerate(pics):
        s.append(shape(t, m + 23 + (k % 5) * 46, m + 23 + (k // 5) * 46, 42))
    svg18 = svg_wrap(2 * m + 5 * 46, 2 * m + 2 * 46, "".join(s), "group of shapes")
    q18 = nums_mcq(fig(svg18) + "How many triangles are there?", ntri, [3, 2, 5],
                   "A triangle has 3 straight sides. Count them all, also the turned ones and the small one: <b>4</b>. "
                   "The quarter circle is not a triangle. It has a curved side.")
    # q19: four quarter circles make a circle
    s, cx, cy, r, g = [], 46, 46, 34, 3
    for rot, (sx, sy) in ((0, (1, -1)), (90, (1, 1)), (180, (-1, 1)), (270, (-1, -1))):
        qx, qy = cx + sx * (r / 2 + g), cy + sy * (r / 2 + g)
        s.append(shape(T("quarter", "green", rot=rot), qx, qy, r / 0.8))
    svg19 = svg_wrap(92, 92, "".join(s), "four quarter circles")
    q19 = mcq(fig(svg19) + "Put these 4 quarter circles together. What shape do they make?", "circle",
              ["square", "half circle", "rectangle"],
              "Each piece is a quarter circle. 4 quarters make a whole <b>circle</b>. 2 of them make a half circle.")
    s = ["<rect x='6' y='6' width='40' height='40' fill='%s' stroke='%s' stroke-width='1.6'/>" % (COLOURS["red"], INK),
         "<rect x='50' y='6' width='40' height='40' fill='%s' stroke='%s' stroke-width='1.6'/>" % (COLOURS["red"], INK)]
    svg20 = svg_wrap(96, 52, "".join(s), "two squares")
    q20 = mcq(fig(svg20) + "Put these 2 squares side by side. What shape do they make?", "rectangle",
              ["square", "triangle", "circle"],
              "The new shape has 2 long sides and 2 short sides. It is a <b>rectangle</b>, not a bigger square.")
    out = [q1, q2, q3, q4, q5, q6, q7, q12, q8, q10, q9, q11, q13, q16, q15, q14, q17, q19, q20, q18]
    assert len({id(x) for x in out}) == 20
    return {"title": "Name the 2D shapes", "items": out}


# ============================================================ set 2: what comes next? (shape and colour)
SC = ("col", "kind")


def set_next():
    A = pat(["circle", "square"], "red")
    B = pat("tri", ["blue", "yellow"])
    Cp = pat(["tri", "circle", "rect"], "green")
    D = pat("square", ["red", "blue", "blue"])
    E = pat(["circle", "tri"], ["yellow", "blue"])
    F = pat(["half", "half", "square"], ["green", "green", "red"])
    G = pat(["circle", "square", "tri"], ["red", "blue", "yellow"])
    H = pat(["circle", "tri", "square"], ["red", "red", "blue"])
    I = pat(["quarter", "circle", "circle"], ["blue", "yellow", "yellow"])
    J = pat(["square", "square", "circle", "circle"], ["blue", "blue", "yellow", "yellow"])
    S = pat(["rect", "tri", "circle"], ["yellow", "green", "green"])

    q1 = next_text(A, 7, SC, tail=" A circle is always followed by a square.")
    q2 = next_text(B, 8, SC, tail=" Only the colour changes. The shape is always a triangle.")
    q3 = next_text(Cp, 7, SC)
    q4 = next_text(D, 8, SC, tail=" After red come two blues. The row ends with red, blue, so one more blue comes next.")
    q5 = next_text(E, 7, SC, tail=" Look at the shape and the colour.")
    q6 = next_text(F, 8, SC, tail=" There are two green half circles in each core, not one.")
    q7 = next_text(G, 7, SC)
    q8 = next_text(H, 6, SC, extra=["red triangle"],
                   tail=" Red triangle has the right colour but the wrong shape. Look at the shape too, not only the colour.")
    q9 = next_text(I, 7, SC, tail=" There are two yellow circles in each core.")
    q10 = next_text(J, 9, SC, tail=" Two blue squares, then two yellow circles.")
    q11 = next_text(S, 7, SC, extra=["green circle"],
                    tail=" Green circle has the right colour but the wrong shape.")

    K = pat(["circle", "square", "square"], "red")
    q12 = mcq(fig(row_svg(toks(K, 9))) + "What is the core of this pattern?", "circle, square, square",
              ["circle, square", "circle, square, square, circle", "square, square"],
              "The core is the part that repeats: <b>circle, square, square</b>. “circle, square” is too short. "
              "After a circle come two squares.")
    Lp = pat("circle", ["blue", "blue", "green"])
    q13 = mcq(fig(row_svg(toks(Lp, 9))) + "What is the core of this pattern?", "blue, blue, green",
              ["blue, green", "blue, blue, green, blue", "blue, blue"],
              "The colours go blue, blue, green, then start again. The core is <b>blue, blue, green</b>. "
              "“blue, blue, green, blue” is too long. It goes into the next core.")
    Mp = pat("tri", ["red", "red", "yellow", "yellow"])
    q14 = nums_mcq(fig(row_svg(toks(Mp, 8))) + "How many shapes are in the core of this pattern?", 4, [2, 8, 3],
                   "The core is red, red, yellow, yellow. That is <b>4</b> shapes. 2 is the number of colours, not shapes.")
    N = pat(["square", "circle", "circle"], ["blue", "red", "red"])
    assert [tok(N, 6), tok(N, 7)] == [T("square", "blue"), T("circle", "red")]
    q15 = mcq(fig(row_svg(toks(N, 6) + ["?", "?"])) + "The pattern repeats. What are the next two shapes?",
              "blue square, red circle",
              ["red circle, red circle", "red circle, blue square", "blue square, blue square"],
              "The core is blue square, red circle, red circle. The row ends with a full core. "
              "So it starts again: <b>blue square, red circle</b>.")
    O = pat(["tri", "square"], "yellow")
    bad = toks(O, 8)
    assert bad[5] == T("square", "yellow")
    bad[5] = T("tri", "yellow")
    q16 = mcq(fig(row_svg(bad, numbered=True)) + "Ethan makes a pattern: triangle, square. "
              "He makes one mistake. Which shape is wrong?", "shape 6", ["shape 5", "shape 7", "shape 8"],
              "Triangles go at 1, 3, 5 and 7. Squares go at 2, 4, 6 and 8. <b>Shape 6</b> is a triangle, "
              "so it is the mistake.")
    P = pat(["tri", "half", "half"], "red")
    q17 = mcq(fig(row_svg(toks(P, 6))) + "Which letters show the same pattern?", "A B B A B B",
              ["A B A B A B", "A A B A A B", "A B C A B C"],
              "Triangle is A. Half circle is B. Triangle, half circle, half circle is A, B, B. "
              "So it is <b>A B B A B B</b>.")
    Q = pat("square", ["green", "green", "red", "red"])
    q18 = mcq(fig(row_svg(toks(Q, 8))) + "Which letters show the same pattern?", "A A B B A A B B",
              ["A B A B A B A B", "A A B A A B A A", "A B B A A B B A"],
              "Green is A. Red is B. Two green, two red: A, A, B, B. So it is <b>A A B B A A B B</b>.")
    q19 = nums_mcq("Ali makes a pattern with paper shapes: square, circle, circle. He makes the core 4 times. "
                   "How many circles does he use?", 8, [4, 12, 3],
                   "Each core has 2 circles. 4 cores: 2 + 2 + 2 + 2 = <b>8</b> circles. "
                   "4 counts only 1 circle in each core.")
    Tp = pat(["circle", "square", "square"], ["red", "blue", "blue"])
    a20 = tok(Tp, 8)
    assert a20 == T("square", "blue")
    q20 = mcq("Hui Min sticks shapes on a card for Children’s Day: red circle, blue square, blue square, red circle, "
              "blue square, blue square … What is the 9th shape?", name(a20, SC),
              ["red circle", "blue circle", "red square"],
              "The core has 3 shapes. Red circles are at 1, 4 and 7. Then 8 and 9 are blue squares. "
              "So the 9th shape is a <b>blue square</b>.")
    out = [q1, q2, q3, q4, q12, q5, q13, q6, q17, q7, q14, q9, q8, q18, q10, q15, q11, q16, q19, q20]
    assert len({id(x) for x in out}) == 20
    return {"title": "What comes next? Shape and colour", "items": out}


# ============================================================ set 3: size and turned shapes
SK = ("size", "kind")


def set_turns():
    q1 = next_text(pat("circle", "blue", ["big", "small"]), 7, SK, tail=" Only the size changes.")
    q2 = next_text(pat("square", "green", ["big", "big", "small"]), 8, SK,
                   tail=" There are two big squares in each core, then one small square.")
    q3 = next_text(pat("tri", "yellow", ["small", "big", "big"]), 7, SK)
    q4 = next_pic(pat("tri", "red", rot=[0, 180]), 7, tail=" The triangle turns over each time.")
    q5 = next_pic(pat("half", "blue", rot=[0, 180]), 6)
    q6 = next_pic(pat("rect", "green", rot=[0, 90]), 7, tail=" The rectangle is lying down, then standing up.")
    q7 = next_pic(pat("square", "yellow", rot=[0, 45]), 6, tail=" A turned square is still a square.")
    p8 = pat("tri", "blue", rot=[0, 90, 180, 270])
    q8 = mcq(fig(row_svg(toks(p8, 8))) + "How does the triangle change each time?", "It turns.",
             ["It changes colour.", "It changes size.", "It changes shape."],
             "Every shape is a blue triangle of the same size. It points up, right, down, left. "
             "So <b>it turns</b> a quarter turn each time.")
    p9 = pat("half", "red", ["big", "small", "small"])
    q9 = mcq(fig(row_svg(toks(p9, 9))) + "How does the half circle change?", "It changes size.",
             ["It turns.", "It changes colour.", "It changes shape."],
             "Every shape is a red half circle with the curved side up. One is big, two are small. "
             "So <b>it changes size</b>.")
    q10 = next_pic(pat("tri", "green", rot=[0, 90, 180, 270]), 6,
                   tail=" The triangle turns a quarter turn each time, like the hands of a clock.")
    q11 = next_pic(pat("quarter", "blue", rot=[0, 90, 180, 270]), 7,
                   tail=" The quarter circle turns a quarter turn each time.")
    q12 = next_pic(pat("half", "yellow", rot=[0, 0, 180]), 7)
    q13 = next_pic(pat("tri", "red", ["big", "small", "small"]), 6,
                   wrong=[T("tri", "red", "small"), T("circle", "red"), T("square", "red")],
                   tail=" Look at the size as well as the shape.")
    q14 = next_pic(pat("half", "green", rot=[0, 90, 180, 270]), 5,
                   tail=" The curved side turns a quarter turn each time.")
    p15 = pat("square", "red", ["big", "small", "small"])
    q15 = mcq(fig(row_svg(toks(p15, 9))) + "What is the core of this pattern?", "big, small, small",
              ["big, small", "big, small, small, big", "small, small"],
              "The sizes go big, small, small, then start again. The core is <b>big, small, small</b>. "
              "“big, small” is too short.")
    p16 = pat("tri", "yellow", rot=[0, 90, 180, 270])
    bad = toks(p16, 8)
    assert bad[5] == T("tri", "yellow", rot=90)
    bad[5] = T("tri", "yellow", rot=270)
    q16 = mcq(fig(row_svg(bad, numbered=True)) + "The triangle should turn a quarter turn each time. "
              "One triangle is wrong. Which one?", "shape 6", ["shape 5", "shape 7", "shape 2"],
              "The triangle points up, right, down, left, then again. Shape 6 should point right. "
              "It points left, so <b>shape 6</b> is wrong.")
    p17 = pat("quarter", "green", rot=[0, 90, 180, 270])
    q17 = nums_mcq(fig(row_svg(toks(p17, 8))) + "How many shapes are in the core of this pattern?", 4, [2, 8, 1],
                   "The quarter circle turns 4 times, then it is back where it started. The core has <b>4</b> shapes.")
    q18 = next_pic(pat("tri", "blue", rot=[0, 0, 180, 180]), 9,
                   tail=" Two point up, then two point down.")
    p19 = pat("quarter", "red", rot=[0, 90, 180, 270])
    a19 = tok(p19, 8)
    q19 = pic_q(toks(p19, 4), "Kumar puts quarter circle tiles in a row. Each tile turns a quarter turn. "
                "These are the first 4 tiles. What does the 9th tile look like?", a19,
                [T("quarter", "red", rot=90), T("quarter", "red", rot=180), T("quarter", "red", rot=270)],
                "The core has 4 tiles. Tiles 1, 5 and 9 look the same. So the 9th tile looks like the 1st: <b>{L}</b>.")
    q20 = next_pic(pat("half", "blue", rot=[270, 90, 90]), 8)
    out = [q1, q4, q2, q5, q8, q6, q3, q7, q9, q13, q10, q15, q12, q17, q11, q14, q18, q16, q20, q19]
    assert len({id(x) for x in out}) == 20
    return {"title": "Patterns with size and turned shapes", "items": out}


# ============================================================ set 4: the missing shape
def set_missing():
    q1 = miss_text(pat(["circle", "square"], "red"), 8, 3, SC)
    q2 = miss_text(pat("tri", ["red", "blue", "blue"]), 9, 4, SC)
    q3 = miss_text(pat(["square", "tri", "circle"], "blue"), 9, 4, SC)
    q4 = miss_text(pat(["half", "half", "rect"], ["yellow", "yellow", "green"]), 9, 5, SC)
    q5 = miss_text(pat("square", "red", ["big", "small"]), 8, 3, SK)
    q6 = miss_pic(pat("tri", "green", rot=[0, 180]), 8, 4)
    q7 = miss_pic(pat("tri", "red", rot=[0, 90, 180, 270]), 8, 5)
    q8 = miss_pic(pat("quarter", "yellow", rot=[0, 90, 180, 270]), 8, 2)
    q9 = miss_text(pat(["circle", "square", "tri"], ["yellow", "red", "blue"]), 9, 4, SC)
    q10 = miss_text(pat("circle", ["green", "green", "blue", "blue"]), 10, 5, SC)
    p11 = pat(["square", "circle"], ["blue", "red"])
    row = toks(p11, 8)
    assert row[2] == T("square", "blue") and row[5] == T("circle", "red")
    row[2] = row[5] = "?"
    q11 = mcq(fig(row_svg(row)) + "Two shapes are missing. What are they, in order?", "blue square, red circle",
              ["red circle, blue square", "blue square, blue square", "red circle, red circle"],
              "The core is blue square, red circle. Shape 3 is a blue square. Shape 6 is a red circle. "
              "So the answer is <b>blue square, red circle</b>.")
    q12 = miss_pic(pat("half", "red", rot=[0, 180, 180]), 9, 4)
    q13 = miss_pic(pat("rect", "blue", rot=[0, 90]), 8, 3)
    q14 = miss_text(pat(["circle", "tri", "square"], ["red", "red", "blue"]), 9, 4, SC, extra=["red circle"],
                    tail=" Red circle has the right colour but the wrong shape.")
    q15 = miss_text(pat("tri", "green", ["big", "small", "small"]), 9, 5, SK)
    q16 = miss_pic(pat("square", "green", rot=[0, 45, 45]), 9, 4)
    p17 = pat("tri", ["yellow", "green", "green"])
    row = toks(p17, 9)
    assert row[3] == T("tri", "yellow") and row[4] == T("tri", "green")
    row[3] = row[4] = "?"
    q17 = mcq(fig(row_svg(row)) + "Two shapes are missing. What are they, in order?",
              "yellow triangle, green triangle",
              ["green triangle, yellow triangle", "green triangle, green triangle", "yellow triangle, yellow triangle"],
              "The colours go yellow, green, green. Shape 3 is green, so a new core starts at shape 4: "
              "<b>yellow triangle, green triangle</b>.")
    q18 = miss_pic(pat("half", "blue", rot=[0, 90, 180, 270]), 8, 6)
    pb = pat("circle", ["red", "yellow", "blue"])
    row = toks(pb, 9)
    assert row[4][1] == "yellow"
    row[4] = "?"
    q19 = mcq(fig(row_svg(row)) + "Siti makes a bracelet with beads in a pattern. One bead falls off. "
              "What colour is the missing bead?", "yellow", ["red", "blue", "green"],
              "The colours go red, yellow, blue, then start again. Bead 4 is red, so bead 5 is <b>yellow</b>. "
              "Check: bead 6 is blue.")
    q20 = miss_pic(pat("quarter", "green", rot=[0, 180]), 8, 5,
                   lead="Mr Tan puts a row of tiles on the kitchen wall of his HDB flat. One tile is missing. "
                        "Which tile goes in the gap?")
    out = [q1, q2, q3, q6, q5, q9, q4, q13, q10, q7, q14, q12, q15, q8, q19, q16, q11, q18, q17, q20]
    assert len({id(x) for x in out}) == 20
    return {"title": "Find the missing shape", "items": out}


# ============================================================ set 5: two things change
SCK = ("size", "col", "kind")


def set_two():
    def which2(p, n, ans, wrong, e):
        return mcq(fig(row_svg(toks(p, n))) + "Which two things change in this pattern?", ans, wrong, e)

    q1 = which2(pat(["circle", "square"], ["red", "blue"]), 8, "shape and colour",
                ["colour only", "shape and size", "size and colour"],
                "The shapes go circle, square. The colours go red, blue. The size stays the same. "
                "So <b>shape and colour</b> change. Do not look only at the colour.")
    q2 = next_text(pat("circle", ["blue", "yellow"], ["big", "small"]), 7, SCK,
                   extra=["big yellow circle"], tail=" Big yellow circle has the right colour but the wrong size.")
    q3 = next_text(pat(["tri", "square"], "green", ["big", "small"]), 7, SK)
    q4 = which2(pat("tri", "blue", ["big", "small"], [0, 180]), 8, "size and turn",
                ["colour and turn", "shape and size", "turn only"],
                "The triangles go big, small. They point up, then down. The colour stays blue. "
                "So <b>size and turn</b> change.")
    q5 = next_pic(pat("tri", ["red", "blue"], rot=[0, 180]), 7,
                  wrong=[T("tri", "red", rot=180), T("tri", "blue"), T("tri", "red")],
                  tail=" Check the colour and the turn.")
    p6 = pat(["circle", "square"], ["red", "blue", "yellow"])
    assert tok(p6, 7) == T("square", "blue")
    q6 = next_text(p6, 7, SC, extra=["blue circle", "red square"],
                   tail=" Even places are squares. The colours start again at shape 7 (red), so shape 8 is blue.")
    p7 = pat(["tri", "circle", "circle"], ["green", "yellow"])
    assert tok(p7, 7) == T("circle", "yellow")
    q7 = next_text(p7, 7, SC, extra=["green circle", "yellow triangle"],
                   tail=" Work out the shape and the colour one at a time.")
    p8 = pat("square", ["red", "red", "blue"], ["big", "small"])
    assert tok(p8, 4) == T("square", "red", "big")
    q8 = miss_text(p8, 9, 4, SCK, extra=["small red square", "big blue square"])
    q9 = next_pic(pat("half", "green", ["big", "big", "small"], [0, 180]), 8,
                  wrong=[T("half", "green", "big"), T("half", "green", "small", 180), T("half", "green", "big", 180)])
    p10 = pat(["circle", "tri"], ["blue", "blue", "yellow"])
    a10 = tok(p10, 9)
    assert a10 == T("tri", "blue")
    q10 = mcq(fig(row_svg(toks(p10, 6))) + "The pattern keeps going. What is the 10th shape?", name(a10, SC),
              ["yellow triangle", "blue circle", "yellow circle"],
              "The shapes go circle, triangle, so even places are triangles. The colours go blue, blue, yellow, "
              "so yellow is at 3, 6 and 9. The 10th shape is a <b>blue triangle</b>.")
    p11 = pat(["rect", "circle"], ["red", "red", "yellow", "yellow"])
    assert tok(p11, 8) == T("rect", "red")
    q11 = next_text(p11, 8, SC, lead="Priya sticks paper shapes on the classroom wall for Children’s Day. "
                    "What comes next?", extra=["red circle", "yellow rectangle"])
    q12 = next_pic(pat("quarter", ["blue", "green"], rot=[0, 90, 180, 270]), 6,
                   wrong=[T("quarter", "green", rot=180), T("quarter", "blue", rot=270), T("quarter", "blue", rot=90)])
    q13 = which2(pat("square", ["yellow", "red"], ["big", "small"]), 8, "size and colour",
                 ["colour only", "shape and colour", "size only"],
                 "The sizes go big, small. The colours go yellow, red. Every shape is a square. "
                 "So <b>size and colour</b> change. Look at the size, not only the colour.")
    q14 = miss_pic(pat("rect", ["yellow", "yellow", "red"], rot=[0, 90]), 8, 4,
                   wrong=[T("rect", "yellow", rot=90), T("rect", "red"), T("rect", "red", rot=90)])
    p15 = pat(["square", "tri", "circle"], "blue", ["big", "small"])
    assert tok(p15, 8) == T("circle", "blue", "big")
    q15 = next_text(p15, 8, SK, extra=["small circle", "big triangle", "small square"])
    q16 = next_pic(pat("tri", "red", ["big", "small"], [0, 90, 180, 270]), 7,
                   wrong=[T("tri", "red", "big", 270), T("tri", "red", "small"), T("tri", "red", "small", 180)])
    p17 = pat("circle", ["red", "blue"], ["big", "small", "small"])
    a17 = tok(p17, 11)
    assert a17 == T("circle", "blue", "small")
    q17 = mcq(fig(row_svg(toks(p17, 6))) + "The pattern keeps going. What is the 12th shape?", name(a17, SCK),
              ["small red circle", "big blue circle", "big red circle"],
              "The colours go red, blue, so even places are blue. The sizes go big, small, small, so big is at "
              "1, 4, 7 and 10. Then 11 and 12 are small. The 12th shape is a <b>small blue circle</b>.")
    p18 = pat(["circle", "square"], ["red", "yellow"], ["big", "small"])
    n18 = sum(1 for t in toks(p18, 9) if t == T("square", "yellow", "small"))
    assert n18 == 4
    q18 = nums_mcq("Jun Jie draws shapes on a Chinese New Year card: big red circle, small yellow square, big red circle, "
                   "small yellow square … He draws 9 shapes. How many are small yellow squares?", n18, [5, 9, 3],
                   "The small yellow squares are at 2, 4, 6 and 8. That is <b>4</b>. "
                   "5 counts the big red circles at 1, 3, 5, 7 and 9.")
    p19 = pat(["circle", "tri", "square"], ["red", "blue"])
    a19 = tok(p19, 6)
    assert a19 == T("circle", "red")
    q19 = mcq("Mdm Wong makes a pattern. The shapes go circle, triangle, square, then start again. "
              "The colours go red, blue, then start again. What is the 7th shape?", name(a19, SC),
              ["blue circle", "red triangle", "red square"],
              "Shapes: circle, triangle, square, circle, triangle, square, circle. Colours: red, blue, red, blue, "
              "red, blue, red. So the 7th shape is a <b>red circle</b>.")
    q20 = miss_pic(pat("half", "yellow", ["big", "small"], [0, 90, 180, 270]), 8, 5,
                   lead="Farah makes a pattern with half circle stickers. One sticker is missing. Which one goes in the box?",
                   wrong=[T("half", "yellow", "big", 90), T("half", "yellow", "small", 270), T("half", "yellow", "small", 180)])
    out = [q1, q2, q3, q5, q13, q4, q6, q8, q7, q9, q11, q14, q15, q10, q12, q16, q18, q17, q19, q20]
    assert len({id(x) for x in out}) == 20
    return {"title": "Patterns where two things change", "items": out}


# ============================================================ lesson
def shapes_chart():
    six = [(T("rect", "yellow"), "rectangle"), (T("square", "red"), "square"), (T("tri", "green"), "triangle"),
           (T("circle", "blue"), "circle"), (T("half", "red"), "half circle"), (T("quarter", "green"), "quarter circle")]
    s, cw, ch = [], 124, 84
    for k, (t, lab) in enumerate(six):
        x, y = 4 + (k % 3) * cw, 4 + (k // 3) * ch
        s.append(shape(t, x + cw / 2, y + 28, 52))
        s.append(text(x + cw / 2, y + 74, lab, 15))
    return svg_wrap(4 * 2 + 3 * cw, 4 * 2 + 2 * ch, "".join(s), "six 2D shapes")


def body_html():
    two = pat(["circle", "square"], ["red", "blue", "yellow"])
    return (
        "<h2>The 2D shapes</h2>"
        "<p>Count the sides and the corners. Look for curved sides.</p>"
        "<figure class='sn-fig'>" + shapes_chart() +
        "<figcaption>A half circle has 1 straight side. A quarter circle has 2 straight sides.</figcaption></figure>"
        + table(["Shape", "Straight sides", "Curved sides"], [
            ["rectangle", "4 (2 long, 2 short)", "0"], ["square", "4 (all the same)", "0"],
            ["triangle", "3", "0"], ["circle", "0", "1"], ["half circle", "1", "1"], ["quarter circle", "2", "1"]])
        + "<p>A turned shape keeps its name. A square that is turned is still a square.</p>"
        "<h2>Repeating patterns and the core</h2>"
        "<p>A repeating pattern has a part that repeats again and again. That part is the <b>core</b>. "
        "Find the core. Then say the pattern out loud to check it.</p>"
        "<figure class='sn-fig'>" + row_svg(toks(pat(["circle", "square", "square"], ["red", "blue", "blue"]), 6) + ["?"]) +
        "<figcaption>The core is red circle, blue square, blue square. Next comes a red circle.</figcaption></figure>"
        "<h2>Size and turns</h2>"
        "<p>A pattern can change the size (big, small) or the way a shape is turned.</p>"
        "<figure class='sn-fig'>" + row_svg(toks(pat("tri", "green", rot=[0, 90, 180, 270]), 6) + ["?"]) +
        "<figcaption>The triangle turns a quarter turn each time: up, right, down, left. Next it points down.</figcaption></figure>"
        "<h2>When two things change</h2>"
        "<p>Look at one thing at a time. First the shape. Then the colour (or the size).</p>"
        "<figure class='sn-fig'>" + row_svg(toks(two, 6) + ["?"]) +
        "<figcaption>The shapes go circle, square. The colours go red, blue, yellow.</figcaption></figure>"
        + ex("Two things change", "What comes next in the pattern above?",
             "Shape 7: the shapes go circle, square, so it is a circle. The colours go red, blue, yellow, "
             "so shape 7 is red.", "red circle")
        + ex("Missing shape", "red, blue, blue, red, ☐, blue, red",
             "The core is red, blue, blue. After red come two blues.", "blue") +
        "<h2>Common mistakes</h2>"
        + table(["Mistake", "What to do instead"], [
            ["Wrong core: red, blue, blue has the core “red, blue”", "Say the pattern again and again to check"],
            ["Only looking at the colour", "Check the shape, the size and the turn too"],
            ["A turned square is “not a square”", "Count the sides. Turning does not change the name"],
            ["Repeating the last shape", "Find where the row stops in the core, then take the next one"],
        ])
    )


FAQ = [
    {"q": "What 2D shapes are taught in Primary 2 maths?",
     "a": "Primary 2 students name and describe rectangles, squares, triangles, circles, half circles and quarter circles. They also make and complete patterns with these shapes."},
    {"q": "How do I help my child with shape patterns?",
     "a": "Ask your child to find the core, the part that repeats, and say it out loud. Then check the shape, colour, size and turn one at a time."},
    {"q": "What is the most common mistake in pattern questions?",
     "a": "Children often look only at the colour and pick a shape with the right colour but the wrong shape. Another mistake is a core that is too short, like “red, blue” for red, blue, blue."},
    {"q": "Is this in the MOE syllabus?",
     "a": "Yes. Making and completing patterns with 2D shapes by size, shape, colour and orientation is part of Geometry in the MOE 2021 Primary 2 Mathematics syllabus."},
]


def gen():
    rnd = random.Random(62811)
    sets = [set_names(), set_next(), set_turns(), set_missing(), set_two()]
    balance(sets, rnd)
    allk = set()
    for s in sets:
        assert len(s["items"]) == 20, (s["title"], len(s["items"]))
        assert sorted(it["a"] for it in s["items"]) == sorted([0, 1, 2, 3] * 5)
        for it in s["items"]:
            assert len(set(it["c"])) == 4, it
            assert it["q"].count("<svg") <= 1
            assert it["q"] not in allk, it["q"]
            allk.add(it["q"])
    u = {
        "country": "sg", "subject": "maths", "grade": "primary-2", "slug": "2d-shapes-and-patterns",
        "sort": 11, "updated": UPDATED, "pdf_url": "",
        "title": "Primary 2 Shapes and Patterns: 2D Shapes, Colour, Size and Turns",
        "seo_title": "P2 2D Shapes and Patterns Worksheets: Free Primary 2 Maths with Answers (MOE Syllabus)",
        "short_title": "2D shapes and patterns",
        "domain": "Measurement and Geometry",
        "standard_code": "Primary 2: Geometry",
        "standard_url": "https://www.moe.gov.sg/primary/curriculum/syllabus",
        "standard_text": "Making and completing patterns with 2D shapes according to size, shape, colour and orientation",
        "meta_desc": "Free P2 maths practice: name 2D shapes and complete patterns by shape, colour, size and turns. 100 questions with answers.",
        "key_big": "Find the core: the part of the pattern that repeats.",
        "key_sub": "Red circle, blue square, blue square, red circle … The core is red circle, blue square, blue square, so next comes a blue square.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }
    assert len(u["meta_desc"]) <= 160
    return mark_large(u, "(shape pattern|group of shapes|four shapes)")


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
