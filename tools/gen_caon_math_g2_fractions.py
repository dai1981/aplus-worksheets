# -*- coding: utf-8 -*-
"""
CA Grade 2 Math: Fractions and Fair Shares (Ontario Mathematics Curriculum 2020, B1.6, B1.7)
  python3 tools/gen_caon_math_g2_fractions.py
Halves, thirds, fourths and sixths of shapes (equal parts), fair-share problems sharing up to 10 items
among 2, 3, 4 and 6 sharers with whole-number, mixed-number and fractional results, comparing shares
(more sharers, smaller shares) and one third = two sixths. Grade 2: fraction words ("two thirds",
"2 and a half"), not fraction symbols. Canadian English; Ontario term "fourths".
Every choice carries its value; a wrong choice never equals the right value or another wrong one.
HTML attributes use single quotes (no backslashes in the JSON).
"""
import json, math, os, random, re
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "ca-on", "math", "grade-2")
UPDATED = "2026-11-02"
FILL = "#4fae74"      # shaded part
RED = "#d6453b"
LINE = "#2b2b2b"
WORD = {2: "halves", 3: "thirds", 4: "fourths", 6: "sixths"}
ONE = {2: "half", 3: "third", 4: "fourth", 6: "sixth"}
NUM = {1: "one", 2: "two", 3: "three", 4: "four", 5: "five", 6: "six"}


# ------------------------------------------------------------ amounts in words
def amt(r, n):
    """r pieces of size 1/n in words: one third, two thirds, one half."""
    return "%s %s" % (NUM[r], ONE[n] if r == 1 else WORD[n])


def mixw(w, r, n):
    if r == 0:
        return str(w)
    if w == 0:
        return amt(r, n)
    if n == 2 and r == 1:
        return "%d and a half" % w
    return "%d and %s" % (w, amt(r, n))


def A(w, r, n):
    return (mixw(w, r, n), F(w) + F(r, n))


def Nc(n, unit=""):
    return ("%d%s" % (n, unit), F(n))


# ------------------------------------------------------------ helpers
class Spots:
    """Where the right answer goes: A-D used equally often, in a shuffled order."""
    def __init__(self):
        self.left = []

    def next(self, rnd):
        if not self.left:
            self.left = [0, 1, 2, 3]
            rnd.shuffle(self.left)
        return self.left.pop()


SPOTS = Spots()


def mcq(q, correct, cands, e, rnd):
    """correct and cands are (html, value) pairs (value may be None for words)."""
    if not isinstance(correct, tuple):
        correct = (correct, None)
    cs, cv = correct
    seen, vals, pick = {cs}, set(), []
    if cv is not None:
        vals.add(cv)
    for c in cands:
        if c is None:
            continue
        if not isinstance(c, tuple):
            c = (c, None)
        s, v = c
        if s in seen or not s:
            continue
        if v is not None and (v <= 0 or v in vals):
            continue
        seen.add(s)
        if v is not None:
            vals.add(v)
        pick.append(s)
        if len(pick) == 3:
            break
    assert len(pick) == 3, (q, cs, cands)
    rnd.shuffle(pick)
    pos = SPOTS.next(rnd)
    ch = pick[:pos] + [cs] + pick[pos:]
    return {"q": q, "c": ch, "a": ch.index(cs), "e": e}


def mcq_abcd(q, pos, e):
    """Choices are the picture labels A-D, in order. pos is the right one."""
    return {"q": q, "c": ["A", "B", "C", "D"], "a": pos, "e": e}


def fig(svg):
    return "<div class='qfig'>" + svg + "</div>"


def svg_wrap(w, h, body, label):
    w, h = int(math.ceil(w)), int(math.ceil(h))
    return ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 %d %d' width='%d' height='%d' "
            "role='img' aria-label='%s'>%s</svg>" % (w, h, w, h, label, body))


def table(head, rows):
    h = "".join("<th>%s</th>" % x for x in head)
    b = "".join("<tr>" + "".join("<td>%s</td>" % c for c in r) + "</tr>" for r in rows)
    return "<div class='sn-tw'><table class='sn-table'><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>" % (h, b)


def ex(title, q, s, a):
    return ("<div class='sn-ex'><span class='sn-ex-t'>%s</span><p class='sn-ex-q'>%s</p>"
            "<p class='sn-ex-s'>%s</p><p class='sn-ex-a'>Answer: %s</p></div>" % (title, q, s, a))


def mark_large(u, pattern):
    """Tag pictures that must print larger so their labels stay readable."""
    rx = re.compile(r"<svg (?=[^>]*aria-label='" + pattern + ")")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u


# ------------------------------------------------------------ pictures
def txt(x, y, s, size=16, anchor="middle", weight="700"):
    return ("<text x='%.1f' y='%.1f' font-size='%d' font-weight='%s' fill='%s' text-anchor='%s'>%s</text>"
            % (x, y, size, weight, LINE, anchor, s))


def att(i, sh, sw=2.5):
    return "fill='%s' stroke='%s' stroke-width='%s'" % (FILL if i in sh else "#fff", LINE, sw)


def bar_row(x0, y, W, H, n, sh, widths=None, sw=2.5):
    """n parts (equal unless widths given, as parts of 1). sh: set of shaded part indexes."""
    ws = [w * W for w in widths] if widths else [W / float(n)] * n
    s, x = [], x0
    for i, w in enumerate(ws):
        s.append("<rect x='%.1f' y='%.1f' width='%.2f' height='%.1f' %s/>" % (x, y, w, H, att(i, sh, sw)))
        x += w
    return "".join(s)


def pie(cx, cy, r, n, sh, widths=None, sw=2.5):
    if n == 1:
        return "<circle cx='%.1f' cy='%.1f' r='%.1f' %s/>" % (cx, cy, r, att(0, sh, sw))
    ws = widths or [1.0 / n] * n
    st = [sum(ws[:i]) for i in range(n + 1)]
    s = []
    for i in range(n):
        a0 = math.radians(-90 + 360.0 * st[i])
        a1 = math.radians(-90 + 360.0 * st[i + 1])
        big = 1 if ws[i] > 0.5 else 0
        s.append("<path d='M%.1f %.1f L%.1f %.1f A%.1f %.1f 0 %d 1 %.1f %.1f Z' %s stroke-linejoin='round'/>"
                 % (cx, cy, cx + r * math.cos(a0), cy + r * math.sin(a0), r, r, big,
                    cx + r * math.cos(a1), cy + r * math.sin(a1), att(i, sh, sw)))
    return "".join(s)


def piece(kind, n, sh, x, y, S, widths=None):
    """One shape in an S x S box. kinds: circle, square (upright strips), grid (2 x 2), grid6 (3 x 2),
    diag (2 or 4 triangles), chord (circle cut into 2 unequal parts), bar (long thin rectangle)."""
    if kind == "circle":
        return pie(x + S / 2.0, y + S / 2.0, S / 2.0, n, sh, widths)
    if kind == "chord":
        r = S / 2.0
        cx, cy = x + r, y + r
        d = 0.42 * r
        h = math.sqrt(r * r - d * d)
        return ("<circle cx='%.1f' cy='%.1f' r='%.1f' %s/>" % (cx, cy, r, att(1, sh)) +
                "<path d='M%.1f %.1f A%.1f %.1f 0 0 1 %.1f %.1f Z' %s stroke-linejoin='round'/>"
                % (cx + d, cy - h, r, r, cx + d, cy + h, att(0, sh)))
    if kind == "square":
        return bar_row(x, y, S, S, n, sh, widths)
    if kind == "bar":
        H = S * 0.42
        return bar_row(x, y + (S - H) / 2, S, H, n, sh, widths)
    if kind in ("grid", "grid6"):
        cols, rows = (2, 2) if kind == "grid" else (3, 2)
        cw, ch = S / float(cols), S / float(rows)
        return "".join("<rect x='%.1f' y='%.1f' width='%.2f' height='%.2f' %s/>"
                       % (x + (i % cols) * cw, y + (i // cols) * ch, cw, ch, att(i, sh)) for i in range(cols * rows))
    if kind == "diag":
        TL, TR, BR, BL = (x, y), (x + S, y), (x + S, y + S), (x, y + S)
        C = (x + S / 2.0, y + S / 2.0)
        tris = [(TL, TR, BR), (TL, BR, BL)] if n == 2 else [(TL, TR, C), (TR, BR, C), (BR, BL, C), (BL, TL, C)]
        return "".join("<polygon points='%s' %s stroke-linejoin='round'/>"
                       % (" ".join("%.1f,%.1f" % p for p in t), att(i, sh)) for i, t in enumerate(tris))
    raise ValueError(kind)


def nparts(kind, n):
    return {"grid": 4, "grid6": 6, "chord": 2}.get(kind, n)


def shape_svg(kind, n, sh, widths=None, S=100):
    n = nparts(kind, n)
    eq = "" if kind == "chord" or widths else "equal "
    what = "bar" if kind == "bar" else "circle" if kind in ("circle", "chord") else "square" if kind != "grid6" else "rectangle"
    lab = "%s cut into %d %sparts with %d shaded" % (what, n, eq, len(sh))
    if kind == "bar":
        W, H = 240, 54
        return svg_wrap(W + 12, H + 12, bar_row(6, 6, W, H, n, sh, widths), lab)
    if kind == "grid6":
        cw = 40
        body = "".join("<rect x='%d' y='%d' width='%d' height='%d' %s/>"
                       % (6 + (i % 3) * cw, 6 + (i // 3) * cw, cw, cw, att(i, sh)) for i in range(6))
        return svg_wrap(3 * cw + 12, 2 * cw + 12, body, lab)
    return svg_wrap(S + 12, S + 12, piece(kind, n, sh, 6, 6, S, widths), lab)


def four_svg(specs, S=78):
    """Four shapes A-D in a row, the letter above each. specs: (kind, n, shaded, widths).
    Four bars go in a 2 x 2 layout instead, so they stay big enough to count the parts."""
    s = []
    if all(k == "bar" for k, _, _, _ in specs):
        W, H = 150, 34
        for i, (kind, n, sh, ws) in enumerate(specs):
            x0 = 6 + (i % 2) * (W + 46)
            y0 = 6 + (i // 2) * (H + 20)
            s.append(txt(x0 + 8, y0 + H / 2 + 6, "ABCD"[i], 18))
            s.append(bar_row(x0 + 24, y0, W, H, n, sh, ws))
        return svg_wrap(2 * (W + 24) + 22 + 12, 2 * H + 20 + 12, "".join(s), "four pictures A to D")
    cw = S + 26
    for i, (kind, n, sh, ws) in enumerate(specs):
        x0 = 6 + i * cw
        s.append(txt(x0 + S / 2, 22, "ABCD"[i], 18))
        s.append(piece(kind, nparts(kind, n), sh, x0, 32, S, ws))
    return svg_wrap(6 + 4 * cw - 26 + 6, 32 + S + 6, "".join(s), "four pictures A to D")


def two_bars_svg(n1, k1, n2, k2, W=240, H=40):
    s = bar_row(6, 6, W, H, n1, set(range(k1))) + bar_row(6, 6 + H + 14, W, H, n2, set(range(k2)))
    return svg_wrap(W + 12, 2 * H + 26, s, "two bars of the same size, top bar %d of %d parts shaded, bottom bar %d of %d parts shaded"
                    % (k1, n1, k2, n2))


def share_svg(m, n, kind, per_row=5):
    """m items shared by n people. Whole items go out first; each leftover item is cut into n equal pieces.
    One person's share is shaded."""
    w, r = divmod(m, n)
    s = []
    if kind == "pizza":
        R, cw, ch = 26, 64, 62
    else:
        R, cw, ch = 0, 76, 46
    rows = -(-m // per_row)
    cols = min(m, per_row)
    for i in range(m):
        x0 = 6 + (i % per_row) * cw
        y0 = 6 + (i // per_row) * ch
        if i < w * n:
            parts, sh = 1, ({0} if i < w else set())
        else:
            parts, sh = n, {0}
        if kind == "pizza":
            s.append(pie(x0 + R + 2, y0 + R + 2, R, parts, sh, sw=2))
        else:
            s.append(bar_row(x0, y0, 66, 34, parts, sh, sw=2))
    Wd = 12 + (cols - 1) * cw + (2 * R + 4 if kind == "pizza" else 66)
    Hd = 12 + (rows - 1) * ch + (2 * R + 4 if kind == "pizza" else 34)
    return svg_wrap(Wd, Hd, "".join(s), "shared items: %d %s shared by %d, one share shaded" % (m, kind, n))


# small things to share
def cookie(cx, cy, r=10):
    chips = "".join("<circle cx='%.1f' cy='%.1f' r='1.8' fill='#5a3410'/>" % (cx + dx * r, cy + dy * r)
                    for dx, dy in [(-0.4, -0.3), (0.35, -0.4), (0.1, 0.35), (-0.3, 0.4), (0.5, 0.15)])
    return "<circle cx='%.1f' cy='%.1f' r='%d' fill='#d9a05b' stroke='#8a5a24' stroke-width='1.6'/>%s" % (cx, cy, r, chips)


def apple(cx, cy, r=10):
    return ("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='#6b4423' stroke-width='2' stroke-linecap='round'/>"
            "<circle cx='%.1f' cy='%.1f' r='%d' fill='%s' stroke='%s' stroke-width='1.6'/>"
            % (cx, cy - r + 1, cx + 1.5, cy - r - 4, cx, cy, r, RED, LINE))


THING = {"cookie": cookie, "apple": apple}


def items_svg(m, thing, cols=None):
    """m things in rows of `cols`, not grouped."""
    st = 28
    cols = cols or (m if m <= 6 else 5)
    rows = -(-m // cols)
    s = [THING[thing](6 + st / 2 + (i % cols) * st, 10 + st / 2 + (i // cols) * st) for i in range(m)]
    return svg_wrap(12 + min(m, cols) * st, 14 + rows * st, "".join(s), "%d %ss" % (m, thing))


def plates_body(x0, y0, counts, thing, st=24):
    """Plates side by side; counts[i] things on plate i, 2 per row. Returns (svg, width, height)."""
    rows = max(1, -(-max(counts) // 2))
    pw, ph = 2 * st + 12, rows * st + 14
    s = []
    for p, k in enumerate(counts):
        px = x0 + p * (pw + 8)
        s.append("<rect x='%.1f' y='%.1f' width='%d' height='%d' rx='12' fill='#eef1f4' stroke='#8a96a3' stroke-width='2'/>"
                 % (px, y0, pw, ph))
        for i in range(k):
            s.append(THING[thing](px + 6 + st / 2 + (i % 2) * st, y0 + 7 + st / 2 + (i // 2) * st, 9))
    return "".join(s), len(counts) * (pw + 8) - 8, ph


def plates_svg(counts, thing):
    body, w, h = plates_body(6, 6, counts, thing)
    return svg_wrap(w + 12, h + 12, body, "plates of %ss: %s" % (thing, ", ".join(map(str, counts))))


def four_plates_svg(groups, thing):
    """Four plate pictures A-D in a 2 x 2 layout."""
    parts = [plates_body(0, 0, g, thing) for g in groups]
    cw = max(p[1] for p in parts) + 40
    rh = max(p[2] for p in parts)
    s = []
    for i, g in enumerate(groups):
        col, row = i % 2, i // 2
        x0 = 6 + col * cw
        y0 = 6 + row * (rh + 14)
        s.append(txt(x0 + 8, y0 + rh / 2.0 + 6, "ABCD"[i], 18))
        body, _, _ = plates_body(x0 + 26, y0, g, thing)
        s.append(body)
    return svg_wrap(6 + 2 * cw - 14 + 6, 6 + 2 * rh + 14 + 6, "".join(s), "four plate pictures A to D")


UNEQ = {3: [0.2, 0.35, 0.45], 4: [0.15, 0.35, 0.2, 0.3], 6: [0.1, 0.22, 0.12, 0.2, 0.16, 0.2]}


def abcd(rnd, q, good, bad, e_good):
    """good: spec; bad: list of (spec, why). Puts the right picture at the next spot."""
    pos = SPOTS.next(rnd)
    order_ = [x[0] for x in bad[:pos]] + [good] + [x[0] for x in bad[pos:]]
    letters = [L for i, L in enumerate("ABCD") if i != pos]
    why = " ".join("%s %s." % (L, d) for L, (_, d) in zip(letters, bad))
    return mcq_abcd(fig(four_svg(order_)) + q, pos, "%s That is <b>%s</b>. %s" % (e_good, "ABCD"[pos], why))


def abcd_plates(rnd, q, thing, good, bad, e_good):
    pos = SPOTS.next(rnd)
    order_ = [x[0] for x in bad[:pos]] + [good] + [x[0] for x in bad[pos:]]
    letters = [L for i, L in enumerate("ABCD") if i != pos]
    why = " ".join("%s %s." % (L, d) for L, (_, d) in zip(letters, bad))
    return mcq_abcd(fig(four_plates_svg(order_, thing)) + q, pos, "%s That is <b>%s</b>. %s" % (e_good, "ABCD"[pos], why))


# ============================================================ set 1: equal parts
def set_parts(rnd):
    SPOTS.left = []
    its = []
    its.append(abcd(rnd, "Which shape is cut into <b>halves</b>?", ("diag", 2, set(), None),
                    [(("chord", 2, set(), None), "has 2 parts, but they are <b>not equal</b>"),
                     (("square", 3, set(), None), "has 3 equal parts"),
                     (("square", 2, set(), [0.3, 0.7]), "has 2 parts, but they are <b>not equal</b>")],
                    "Halves are <b>2 equal parts</b>."))
    its.append(abcd(rnd, "Which shape is cut into <b>thirds</b>?", ("circle", 3, set(), None),
                    [(("square", 3, set(), UNEQ[3]), "has 3 parts, but they are <b>not equal</b>"),
                     (("grid", 4, set(), None), "has 4 equal parts"),
                     (("square", 2, set(), None), "has 2 equal parts")],
                    "Thirds are <b>3 equal parts</b>."))
    its.append(abcd(rnd, "Which shape is cut into <b>fourths</b>?", ("grid", 4, set(), None),
                    [(("circle", 4, set(), UNEQ[4]), "has 4 parts, but they are <b>not equal</b>"),
                     (("circle", 3, set(), None), "has 3 equal parts"),
                     (("circle", 6, set(), None), "has 6 equal parts")],
                    "Fourths are <b>4 equal parts</b>."))
    its.append(abcd(rnd, "Which shape is cut into <b>sixths</b>?", ("circle", 6, set(), None),
                    [(("diag", 4, set(), None), "has 4 equal parts"),
                     (("square", 6, set(), UNEQ[6]), "has 6 parts, but they are <b>not equal</b>"),
                     (("square", 3, set(), None), "has 3 equal parts")],
                    "Sixths are <b>6 equal parts</b>."))
    its.append(abcd(rnd, "Which shape is <b>not</b> cut into equal parts?", ("square", 3, set(), UNEQ[3]),
                    [(("circle", 6, set(), None), "has 6 equal parts"),
                     (("diag", 4, set(), None), "has 4 equal parts"),
                     (("circle", 2, set(), None), "has 2 equal parts")],
                    "Look for parts that are different sizes."))

    names = ["halves", "thirds", "fourths", "sixths"]
    for kind, n in [("square", 3), ("grid6", 6), ("diag", 4), ("circle", 2), ("bar", 6)]:
        n = nparts(kind, n)
        e = "Count the parts. There are <b>%d equal parts</b>. %d equal parts are called <b>%s</b>." % (n, n, WORD[n])
        its.append(mcq(fig(shape_svg(kind, n, set())) + "The shape is cut into equal parts. What are the parts called?",
                       WORD[n], [x for x in names if x != WORD[n]], e, rnd))

    shaded = [
        ("circle", 3, {0}, (1, 3), [A(0, 2, 3), A(0, 1, 4), A(0, 1, 2)]),
        ("grid", 4, {2}, (1, 4), [A(0, 3, 4), A(0, 1, 3), A(0, 1, 2)]),
        ("bar", 6, {0}, (1, 6), [A(0, 5, 6), A(0, 1, 4), A(0, 1, 3)]),
        ("square", 2, {1}, (1, 2), [A(0, 1, 4), ("two halves", F(1)), A(0, 1, 3)]),
        ("circle", 6, {0, 1}, (2, 6), [A(0, 4, 6), A(0, 1, 6), A(0, 2, 4)]),
    ]
    for kind, n, sh, (k, d), cands in shaded:
        rest = d - k
        e = ("There are <b>%d equal parts</b>, so they are %s. <b>%d</b> %s shaded. So <b>%s</b> is shaded. "
             "Do not count the white parts." % (d, WORD[d], k, "part is" if k == 1 else "parts are", amt(k, d)))
        if k == 2 and d == 6:
            e += " (Two sixths is the same as one third.)"
        its.append(mcq(fig(shape_svg(kind, n, sh)) + "What part of the shape is shaded?", A(0, k, d), cands, e, rnd))

    for n, ws, ok in [(4, UNEQ[4], False), (3, None, True)]:
        svg = shape_svg("bar", n, {0}, ws)
        right = ("Yes. It has %d equal parts." % n) if ok else "No. The parts are not equal."
        cands = ["Yes. It has %d parts." % n, "No. It needs more parts.",
                 ("No. The parts are not equal." if ok else "Yes. It has %d equal parts." % n),
                 "Yes. One part is shaded."]
        e = ("Fractions need <b>equal parts</b>. " +
             ("All 3 parts are the same size, so the shaded part is one third." if ok
              else "These 4 parts are different sizes, so the shaded part is <b>not</b> one fourth."))
        its.append(mcq(fig(svg) + "Is the shaded part <b>%s</b> of the bar?" % amt(1, n), right, cands, e, rnd))

    for n, wrong in [(3, [2, 6, 4]), (6, [3, 4, 5]), (4, [2, 8, 3])]:
        e = "<b>%d</b> equal parts make %s. Each part is one %s." % (n, WORD[n], ONE[n])
        its.append(mcq("How many equal parts make <b>%s</b>?" % WORD[n], Nc(n), [Nc(x) for x in wrong], e, rnd))
    assert len(its) == 20, len(its)
    return {"title": "Halves, thirds, fourths and sixths", "items": its}


# ============================================================ set 2: fair shares, whole numbers
def plus(w, n):
    return " + ".join([str(w)] * n)


def set_whole(rnd):
    SPOTS.left = []
    its = []
    deals = [(4, 2, "cookie", "cookies"), (6, 3, "apple", "apples"), (8, 4, "cookie", "cookies"), (10, 2, "apple", "apples"),
             (6, 6, "cookie", "cookies"), (9, 3, "cookie", "cookies"),
             (8, 2, None, "stickers"), (3, 3, None, "crackers"), (6, 2, None, "hockey cards"), (4, 4, None, "strawberries")]
    for m, n, thing, many in deals:
        w = m // n
        q = "%d %s are shared equally by %d friends. How many %s does each friend get?" % (m, many, n, many)
        if thing:
            q = fig(items_svg(m, thing)) + q
        e = ("Give out the %s one at a time to the %d friends until none are left. Each friend gets <b>%d</b>. "
             "Check: %s = %d." % (many, n, w, plus(w, n), m))
        its.append(mcq(q, Nc(w), [Nc(m), Nc(n), Nc(m - n), Nc(w + 1), Nc(m + n)], e, rnd))

    for m, each, many in [(8, 2, "apples"), (9, 3, "muffins"), (6, 1, "granola bars"), (10, 5, "crackers")]:
        k = m // each
        e = "Make groups of %d until all %d %s are used: %s = %d. That is <b>%d</b> friends." % (each, m, many, plus(each, k), m, k)
        its.append(mcq("There are %d %s. Each friend gets %d. How many friends share the %s?" % (m, many, each, many),
                       Nc(k), [Nc(m), Nc(each), Nc(m - each), Nc(k + 1)], e, rnd))

    its.append(abcd_plates(rnd, "Which picture shows <b>6 cookies</b> shared fairly by <b>3 friends</b>?", "cookie",
                           [2, 2, 2], [([3, 2, 1], "has 3 plates, but they are <b>not equal</b>"),
                                       ([3, 3], "has only 2 plates"),
                                       ([2, 2, 1], "has only 5 cookies")],
                           "Fair means <b>3 plates</b> with <b>the same number</b> on each: 2 + 2 + 2 = 6."))
    its.append(abcd_plates(rnd, "Which picture shows <b>8 apples</b> shared fairly by <b>4 friends</b>?", "apple",
                           [2, 2, 2, 2], [([4, 4], "has only 2 plates"),
                                          ([3, 2, 2, 1], "has 4 plates, but they are <b>not equal</b>"),
                                          ([2, 2, 2], "has only 3 plates and 6 apples")],
                           "Fair means <b>4 plates</b> with <b>the same number</b> on each: 2 + 2 + 2 + 2 = 8."))
    its.append(mcq(fig(plates_svg([3, 3, 2], "cookie")) + "Liam put 8 cookies on 3 plates like this. Is it a fair share?",
                   "No. One plate has fewer.", ["Yes. All 8 are on plates.", "Yes. Each plate has some.", "No. There are too many plates."],
                   "A fair share means <b>every plate has the same number</b>. Two plates have 3 and one plate has 2, so it is not fair.", rnd))
    its.append(mcq("7 cookies are shared equally by 2 friends. Each friend gets 3. How many cookies are left over?",
                   Nc(1, " cookie"), [Nc(4, " cookies"), Nc(3, " cookies"), Nc(5, " cookies")],
                   "2 friends get 3 each: 3 + 3 = 6. 7 − 6 = <b>1</b> cookie is left over.", rnd))
    its.append(mcq("10 apples are shared equally by 4 friends. Each friend gets 2. How many apples are left over?",
                   Nc(2, " apples"), [Nc(6, " apples"), Nc(8, " apples"), Nc(4, " apples")],
                   "4 friends get 2 each: 2 + 2 + 2 + 2 = 8. 10 − 8 = <b>2</b> apples are left over.", rnd))
    its.append(mcq("9 muffins are shared equally with <b>none left over</b>. How many friends can share them?",
                   Nc(3, " friends"), [Nc(2, " friends"), Nc(4, " friends"), Nc(6, " friends")],
                   "3 friends get 3 each: 3 + 3 + 3 = 9, none left. With 2, 4 or 6 friends, some muffins are left over.", rnd))
    assert len(its) == 20, len(its)
    return {"title": "Fair shares with whole numbers", "items": its}


# ============================================================ set 3: fair shares with leftovers cut into pieces
ITEM = {"pizza": ("pizza", "pizzas"), "sandwich": ("sandwich", "sandwiches"), "granola": ("granola bar", "granola bars"),
        "pancake": ("pancake", "pancakes"), "muffin": ("muffin", "muffins"), "sub": ("sub", "subs")}


def e_share(m, n, it):
    one, many = ITEM[it]
    w, r = divmod(m, n)
    if m == 1:
        return ("Cut the %s into <b>%d equal pieces</b> (%s). Each friend gets 1 piece: <b>%s</b> of the %s."
                % (one, n, WORD[n], amt(1, n), one))
    if w == 0:
        return ("There are fewer %s than friends. Cut each %s into <b>%s</b>. Each friend gets 1 piece from each %s. "
                "%d %s, so each friend gets <b>%s</b> of a %s." % (many, one, WORD[n], one, m, many, amt(m, n), one))
    left = "1 %s is" % one if r == 1 else "%d %s are" % (r, many)
    return ("Give out whole %s first: %d each, and %s left. Cut %s into <b>%s</b>. Each friend gets %s more. "
            "So each friend gets <b>%s</b> %s." % (many, w, left, "it" if r == 1 else "each one", WORD[n],
                                                  amt(r, n), mixw(w, r, n), many))


def share_cands(m, n):
    w, r = divmod(m, n)
    if w == 0:
        return [A(0, 1, n) if m > 1 else None, A(0, n - m, n) if n - m != m else None, ("1 whole", F(1)),
                A(0, 1, 2), A(0, 1, 3), A(0, 1, 4)]
    return [Nc(w), A(w, 1, n) if r > 1 else None, Nc(w + 1), A(w, n - r, n) if n - r != r else None,
            A(w, 1, 2), A(w, 1, 3)]


def set_leftovers(rnd):
    SPOTS.left = []
    its = []
    for m, n, it in [(1, 3, "pizza"), (2, 3, "sandwich"), (3, 4, "pizza"), (1, 6, "pizza"), (5, 6, "pizza"), (1, 4, "sandwich")]:
        one, many = ITEM[it]
        kind = "pizza" if it == "pizza" else "bar"
        q = (fig(share_svg(m, n, kind)) + "%d %s %s shared equally by %d friends. The shaded part is one friend’s share. "
             "How much %s does each friend get?" % (m, one if m == 1 else many, "is" if m == 1 else "are", n,
                                                   "pizza" if it == "pizza" else "of a " + one))
        its.append(mcq(q, A(*((0,) + divmod(m, n)[1:] + (n,))), share_cands(m, n), e_share(m, n, it), rnd))
    for m, n, it in [(3, 2, "pancake"), (5, 2, "sandwich"), (4, 3, "pizza"), (7, 4, "pizza"), (7, 3, "sandwich"), (7, 6, "pizza")]:
        one, many = ITEM[it]
        kind = "pizza" if it in ("pizza", "pancake") else "bar"
        w, r = divmod(m, n)
        q = (fig(share_svg(m, n, kind, per_row=5 if kind == "pizza" else 4)) +
             "%d %s are shared equally by %d friends. The shaded parts are one friend’s share. How many %s does each friend get?"
             % (m, many, n, many))
        its.append(mcq(q, A(w, r, n), share_cands(m, n), e_share(m, n, it), rnd))
    for m, n, it in [(9, 2, "granola"), (10, 3, "pancake"), (9, 4, "muffin"), (8, 3, "sub")]:
        one, many = ITEM[it]
        w, r = divmod(m, n)
        its.append(mcq("%d %s are shared equally by %d friends. How many %s does each friend get?" % (m, many, n, many),
                       A(w, r, n), share_cands(m, n), e_share(m, n, it), rnd))
    for m, n in [(4, 6), (5, 4)]:
        right = "Less than 1 pizza" if m < n else "More than 1 pizza"
        e = ("Compare the pizzas and the friends. %d pizzas for %d friends: " % (m, n) +
             ("there are <b>fewer pizzas than friends</b>, so each friend gets less than 1 pizza (%s)." % amt(m, n) if m < n
              else "there are <b>more pizzas than friends</b>, so each friend gets 1 pizza and a bit more (%s)." % mixw(1, m - n, n)))
        its.append(mcq("%d friends share %d pizzas equally. Does each friend get more or less than 1 pizza?" % (n, m),
                       right, ["More than 1 pizza" if m < n else "Less than 1 pizza", "Exactly 1 pizza",
                               "Exactly %d pizzas" % m], e, rnd))
    for m, n, it in [(3, 4, "granola"), (5, 6, "pizza")]:
        one, many = ITEM[it]
        e = ("Each %s is cut into %d equal pieces. Each friend gets <b>1 piece from each %s</b>. "
             "There are %d %s, so each friend gets <b>%d %s</b>." % (one, n, one, m, many, m, WORD[n]))
        its.append(mcq("%d friends share %d %s equally. Each %s is cut into %s. How many %s does each friend get?"
                       % (n, m, many, one, WORD[n], WORD[n]),
                       Nc(m, " " + WORD[n]), [Nc(n, " " + WORD[n]), Nc(1, " " + ONE[n]), Nc(n - m, " " + WORD[n]) if n - m > 1 else None,
                                              Nc(m + n, " " + WORD[n])], e, rnd))
    assert len(its) == 20, len(its)
    return {"title": "Fair shares with leftovers", "items": its}


# ============================================================ set 4: compare shares
def set_compare(rnd):
    SPOTS.left = []
    its = []
    for n1, n2 in [(2, 4), (6, 3), (4, 6), (3, 2)]:
        big, small = min(n1, n2), max(n1, n2)
        e = ("The bars are the same size. The top bar has %d parts and the bottom bar has %d parts. "
             "<b>Fewer parts means bigger parts</b>, so one %s is bigger than one %s." % (n1, n2, ONE[big], ONE[small]))
        its.append(mcq(fig(two_bars_svg(n1, 1, n2, 1)) + "The bars are the same size. Which shaded part is bigger?",
                       "one " + ONE[big], ["one " + ONE[small], "They are the same size", "You can’t tell"], e, rnd))
    for a, b, want in [(6, 4, "bigger"), (2, 3, "bigger"), (3, 6, "smaller"), (4, 2, "smaller"), (6, 2, "smaller")]:
        lo, hi = min(a, b), max(a, b)
        ans = lo if want == "bigger" else hi
        oth = hi if want == "bigger" else lo
        e = ("Think of the same pizza. Cut into %d pieces, the pieces are bigger than cut into %d pieces. "
             "So one %s is %s than one %s." % (lo, hi, ONE[ans], want, ONE[oth]))
        its.append(mcq("Same size pizzas. Which piece is <b>%s</b>: one %s or one %s?" % (want, ONE[a], ONE[b]),
                       "one " + ONE[ans], ["one " + ONE[oth], "They are the same size", "You can’t tell"], e, rnd))
    for n1, n2, food, a1, a2 in [(2, 6, "pizza", "Zoe", "Liam"), (4, 3, "pan of brownies", "Maya", "Owen"),
                                 (6, 4, "cake", "Priya", "Noah")]:
        big = a1 if n1 < n2 else a2
        other = a2 if big == a1 else a1
        nb, ns = min(n1, n2), max(n1, n2)
        e = ("The same size %s cut for %d people has bigger pieces than one cut for %d people. "
             "One %s is bigger than one %s, so <b>%s’s group</b> gets bigger pieces." % (food, nb, ns, ONE[nb], ONE[ns], big))
        its.append(mcq("%s’s group of %d shares a %s equally. %s’s group of %d shares the same size %s. "
                       "Whose group gets bigger pieces?" % (a1, n1, food, a2, n2, food),
                       "%s’s group" % big, ["%s’s group" % other, "They get the same size", "You can’t tell"], e, rnd))
    for m, n1, n2, many in [(6, 2, 3, "cookies"), (1, 4, 6, "pizza"), (4, 4, 2, "sandwiches")]:
        lo, hi = min(n1, n2), max(n1, n2)
        what = "a pizza" if m == 1 else "%d %s" % (m, many)
        e = ("Fewer friends means a <b>bigger share</b> for each friend. %s shared by %d gives each friend %s. "
             "Shared by %d, each friend gets %s." % (what[0].upper() + what[1:], lo, mixw(*divmod(m, lo) + (lo,)) if m % lo else str(m // lo),
                                                     hi, mixw(*divmod(m, hi) + (hi,)) if m % hi else str(m // hi)))
        its.append(mcq("%s can be shared equally by %d friends or by %d friends. When does each friend get <b>more</b>?"
                       % (what[0].upper() + what[1:], n1, n2), "Shared by %d friends" % lo,
                       ["Shared by %d friends" % hi, "It is the same", "You can’t tell"], e, rnd))
    its.append(mcq("Which piece is the <b>biggest</b>? All the pizzas are the same size.", "one half",
                   ["one third", "one fourth", "one sixth"],
                   "A pizza cut into 2 pieces has the biggest pieces. <b>One half</b> is the biggest.", rnd))
    its.append(mcq("Which piece is the <b>smallest</b>? All the pizzas are the same size.", "one sixth",
                   ["one half", "one third", "one fourth"],
                   "A pizza cut into 6 pieces has the smallest pieces. <b>One sixth</b> is the smallest.", rnd))
    its.append(mcq("Kai says one sixth of a pizza is bigger than one third of the same pizza, because 6 is more than 3. Is he right?",
                   "No. One third is bigger.", ["Yes. 6 is more than 3.", "No. They are the same.", "Yes. Sixths are bigger."],
                   "6 people share the pizza for sixths, and 3 people share it for thirds. <b>More sharers means smaller pieces.</b> "
                   "So one third is bigger than one sixth.", rnd))
    its.append(mcq("Amira says one fourth of a sandwich is bigger than one half of the same sandwich. Is she right?",
                   "No. One half is bigger.", ["Yes. 4 is more than 2.", "No. They are the same.", "Yes. Fourths are bigger."],
                   "Cut a sandwich into 2 pieces or into 4 pieces. The 2 pieces are bigger. So one half is bigger than one fourth.", rnd))
    order = lambda ns: ", ".join("one " + ONE[x] for x in ns)
    its.append(mcq("Put the pieces in order from <b>biggest to smallest</b>: one sixth, one half, one third",
                   order([2, 3, 6]), [order([6, 3, 2]), order([2, 6, 3]), order([3, 2, 6])],
                   "Fewer pieces means bigger pieces. Halves (2 pieces) are biggest, then thirds (3), then sixths (6): <b>%s</b>." % order([2, 3, 6]), rnd))
    assert len(its) == 20, len(its)
    return {"title": "Compare shares", "items": its}


# ============================================================ set 5: one third and two sixths, word problems
def set_words(rnd):
    SPOTS.left = []
    W = []

    def add(q, right, cands, e):
        W.append((q, right, cands, e))

    add(fig(two_bars_svg(3, 1, 6, 2)) + "The bars are the same size. Is the shaded amount the same?",
        "Yes. They are the same.", ["No. Two sixths is more.", "No. One third is more.", "You can’t tell."],
        "Cut each third in half and you get sixths. <b>One third</b> covers the same space as <b>two sixths</b>.")
    add(fig(two_bars_svg(3, 1, 6, 0)) + "The top bar shows one third. How many sixths cover the same amount?",
        ("two sixths", F(2, 6)), [A(0, 1, 6), A(0, 3, 6), A(0, 4, 6)],
        "Each third is 2 sixths. So one third is the same as <b>two sixths</b>.")
    add("Which bar shows the same amount as <b>one third</b>?", "ABCD",
        (("bar", 6, {0, 1}, None), [(("bar", 6, {0}, None), "shows one sixth"), (("bar", 6, {0, 1, 2}, None), "shows three sixths"),
                                    (("bar", 4, {0, 1}, None), "shows two fourths")]),
        "One third is the same as <b>two sixths</b>.")
    add(fig(two_bars_svg(2, 1, 4, 2)) + "The bars are the same size. The top bar shows one half. What does the bottom bar show?",
        A(0, 2, 4), [A(0, 1, 4), A(0, 3, 4), A(0, 2, 6)],
        "The bottom bar has 4 equal parts and 2 are shaded: <b>two fourths</b>. It is the same as one half.")
    add("One third of a pizza is the same as how many sixths?", A(0, 2, 6), [A(0, 1, 6), A(0, 3, 6), A(0, 4, 6)],
        "Cut each third into 2 equal pieces. One third becomes <b>two sixths</b>.")
    add("Which is the same amount as <b>two sixths</b>?", A(0, 1, 3), [A(0, 2, 3), A(0, 1, 6), A(0, 1, 2)],
        "Two sixths fill the same space as <b>one third</b>. Two thirds would be 4 sixths.")
    add("Owen eats one third of a sub. Ava eats two sixths of the same size sub. Who eats more?",
        "They eat the same amount.", ["Ava, because 2 is more than 1", "Owen, because thirds are big", "You can’t tell."],
        "Two sixths is the same as one third. So they eat <b>the same amount</b>.")
    add("Zoe says two sixths of a pie is more than one third of the same pie, because 2 is more than 1. Is she right?",
        "No. They are the same.", ["Yes. 2 is more than 1.", "No. One third is more.", "Yes. Sixths are bigger."],
        "Sixths are smaller pieces. Two sixths fill the same space as one third, so they are <b>the same</b>.")
    add("A pan of brownies is cut into 6 equal pieces. 3 friends share it fairly. How many pieces does each friend get?",
        Nc(2, " pieces"), [Nc(3, " pieces"), Nc(6, " pieces"), Nc(1, " piece")],
        "6 pieces for 3 friends: 2 + 2 + 2 = 6. Each friend gets <b>2 pieces</b>. That is two sixths, the same as one third.")
    add("Kai cuts a sub into thirds and eats 1 piece. Hana cuts the same size sub into sixths. "
        "How many pieces must Hana eat to eat the same amount as Kai?",
        Nc(2, " pieces"), [Nc(1, " piece"), Nc(3, " pieces"), Nc(6, " pieces")],
        "One third is the same as two sixths. Hana must eat <b>2 pieces</b>.")
    add("On a canoe trip, 2 friends share 5 granola bars equally. How many granola bars does each friend get?",
        A(2, 1, 2), [Nc(2), Nc(3), A(2, 1, 4)],
        "Give out whole bars: 2 each, and 1 bar is left. Cut it in half. Each friend gets <b>2 and a half</b> granola bars.")
    add("At recess, 3 friends share 7 oranges equally. How many oranges does each friend get?",
        A(2, 1, 3), [Nc(2), A(2, 1, 2), Nc(3)],
        "Give out whole oranges: 2 each, and 1 is left. Cut it into thirds. Each friend gets <b>2 and one third</b> oranges.")
    add("After hockey practice, 6 players share 4 oranges equally. How much orange does each player get?",
        A(0, 4, 6), [A(0, 1, 6), A(0, 2, 6), ("1 whole", F(1))],
        "Cut each orange into sixths. Each player gets 1 piece from each of the 4 oranges: <b>four sixths</b> of an orange.")
    add("On a snow day, 4 friends share 3 muffins equally. How much muffin does each friend get?",
        A(0, 3, 4), [A(0, 1, 4), A(0, 1, 3), ("1 whole", F(1))],
        "Cut each muffin into fourths. Each friend gets 1 piece from each of the 3 muffins: <b>three fourths</b> of a muffin.")
    add("At a March Break sleepover, 4 friends share 10 pancakes equally. How many pancakes does each friend get?",
        A(2, 2, 4), [Nc(2), A(2, 1, 4), Nc(3)],
        "Give out whole pancakes: 2 each, and 2 are left. Cut each into fourths. Each friend gets 2 more fourths. "
        "So each friend gets <b>2 and two fourths</b> pancakes (the same as 2 and a half).")
    add("Ethan and Priya share 7 maple cookies equally. How many cookies does each child get?",
        A(3, 1, 2), [Nc(3), Nc(4), A(3, 1, 4)],
        "Give out whole cookies: 3 each, and 1 is left. Cut it in half. Each child gets <b>3 and a half</b> cookies.")
    add("Liam and 2 friends share 9 hockey cards equally. How many cards does each person get?",
        Nc(3, " cards"), [Nc(4, " cards"), Nc(9, " cards"), Nc(6, " cards")],
        "Liam and 2 friends are <b>3 people</b>. 3 + 3 + 3 = 9, so each person gets <b>3 cards</b>.")
    add("At lunch, Emma’s group of 3 shares a pizza. Noah’s group of 6 shares the same size pizza. Whose group gets bigger pieces?",
        "Emma’s group", ["Noah’s group", "They get the same size", "You can’t tell"],
        "Fewer people means bigger pieces. One third is bigger than one sixth, so <b>Emma’s group</b> gets bigger pieces. "
        "Each piece for Emma’s group is as big as 2 pieces for Noah’s group.")
    add("Arjun cuts a pizza into 6 pieces. The pieces are different sizes. He says each piece is one sixth. Is he right?",
        "No. The pieces are not equal.", ["Yes. There are 6 pieces.", "No. Each piece is one third.", "Yes. Each piece is one part."],
        "Sixths must be <b>6 equal parts</b>. The pieces are different sizes, so they are not sixths.")
    add("At Thanksgiving, 6 cousins share 9 pumpkin tarts equally. How many tarts does each cousin get?",
        A(1, 3, 6), [Nc(1), A(1, 1, 6), Nc(2)],
        "Give out whole tarts: 1 each, and 3 are left. Cut each into sixths. Each cousin gets 3 more sixths. "
        "So each cousin gets <b>1 and three sixths</b> tarts (the same as 1 and a half).")
    assert len(W) == 20, len(W)
    its = []
    for q, right, cands, e in W:
        if right == "ABCD":
            its.append(abcd(rnd, q, cands[0], cands[1], e))
            continue
        its.append(mcq(q, right, cands, e, rnd))
    return {"title": "One third is two sixths: word problems", "items": its}


# ============================================================ lesson
def body_html():
    dens = [2, 3, 4, 6]
    LW = 82
    parts_fig = svg_wrap(LW + 252, 6 + len(dens) * 48, "".join(
        [txt(6, 6 + r * 48 + 26, WORD[n], 16, "start") for r, n in enumerate(dens)] +
        [bar_row(LW, 6 + r * 48, 240, 36, n, {0}) for r, n in enumerate(dens)]),
        "bars of the same size cut into halves, thirds, fourths and sixths, one part shaded in each")
    names = table(["Equal parts", "Name", "One part"], [[str(n), WORD[n], "one " + ONE[n]] for n in dens])
    plates = ("<figure class='sn-fig'>" + plates_svg([2, 2, 2], "cookie") +
              "<figcaption>6 cookies shared fairly by 3 friends: 2 + 2 + 2 = 6. Each friend gets 2.</figcaption></figure>")
    share1 = ("<figure class='sn-fig'>" + share_svg(5, 2, "bar") +
              "<figcaption>5 sandwiches shared by 2 friends. Each gets 2 whole sandwiches. The last one is cut in half. "
              "Each friend gets 2 and a half sandwiches.</figcaption></figure>")
    share2 = ("<figure class='sn-fig'>" + share_svg(2, 3, "pizza") +
              "<figcaption>2 pizzas shared by 3 friends. Cut each pizza into thirds. One friend gets the shaded pieces: "
              "two thirds of a pizza.</figcaption></figure>")
    eq_fig = ("<figure class='sn-fig'>" + two_bars_svg(3, 1, 6, 2) +
              "<figcaption>One third and two sixths cover the same amount.</figcaption></figure>")
    return (
        "<h2>Equal parts</h2>"
        "<p>A fraction is <b>part of a whole</b>. The parts must be <b>equal</b>: all the same size.</p>"
        "<p>2 equal parts are <b>halves</b>. 3 equal parts are <b>thirds</b>. 4 equal parts are <b>fourths</b>. "
        "6 equal parts are <b>sixths</b>.</p>"
        "<figure class='sn-fig'>" + parts_fig + "<figcaption>One part is shaded in each bar.</figcaption></figure>"
        + names +
        "<h2>Fair shares</h2>"
        "<p>A fair share means everyone gets <b>the same amount</b>. Give the items out one at a time until none are left.</p>"
        + plates +
        "<p>Sometimes items are left over. Cut each leftover item into as many equal pieces as there are friends.</p>"
        + share1 + share2 +
        ex("Example", "8 apples are shared by 4 friends.", "Give them out one at a time. 2 + 2 + 2 + 2 = 8.", "2 apples each")
        + ex("Example", "7 oranges are shared by 3 friends.",
             "Each friend gets 2 whole oranges. 1 orange is left. Cut it into thirds.", "2 and one third oranges each")
        + "<h2>Compare shares</h2>"
        "<p><b>More sharers means smaller shares.</b> A pizza for 6 people has smaller pieces than a pizza for 3 people. "
        "So one sixth is smaller than one third.</p>"
        + ex("Example", "Which is bigger: one fourth or one half of the same sandwich?",
             "2 pieces are bigger than 4 pieces.", "one half")
        + "<h2>One third is two sixths</h2>"
        "<p>Cut each third in half and you get sixths. So <b>one third</b> is the same amount as <b>two sixths</b>.</p>"
        + eq_fig
        + "<h2>Common mistakes</h2>"
        + table(["Mistake", "What to do instead"], [
            ["Calling unequal parts “fourths” or “thirds”", "The parts must be <b>equal</b>"],
            ["Thinking one sixth is bigger than one third because 6 is bigger than 3",
             "More pieces means <b>smaller</b> pieces, so one sixth is smaller"],
            ["Thinking two sixths is more than one third because 2 is more than 1", "They are the <b>same</b> amount"],
            ["Forgetting the leftover: 5 sandwiches for 2 is “2 each”", "Cut the leftover too: 2 and a half each"],
            ["Counting the white parts: 1 of 3 parts shaded is “two thirds”", "Count the <b>shaded</b> parts: one third"],
            ["Forgetting to count yourself: “Liam and 2 friends” is 2 people", "Count everyone who shares: 3 people"],
        ])
    )


FAQ = [
    {"q": "What fractions do Grade 2 students learn in Ontario?",
     "a": "In the Ontario math curriculum, Grade 2 students work with halves, thirds, fourths and sixths. They use drawings to share up to 10 items among 2, 3, 4 or 6 people, and they learn that one third is the same as two sixths."},
    {"q": "What is a fair-share problem in Grade 2 math?",
     "a": "A fair-share problem shares items equally, like 5 sandwiches shared by 2 friends. Each friend gets 2 whole sandwiches, and the last one is cut in half, so each gets 2 and a half."},
    {"q": "Why is one sixth smaller than one third?",
     "a": "Share the same pizza with 6 people and with 3 people. With more people each piece is smaller, so one sixth is smaller than one third."},
    {"q": "Is one third the same as two sixths?",
     "a": "Yes. Cut each third of a shape in half and you get sixths, so one third covers the same amount as two sixths. Drawing two bars of the same size is an easy way to show it."},
]


def gen():
    rnd = random.Random(42807)
    SPOTS.left = []
    sets = [set_parts(rnd), set_whole(rnd), set_leftovers(rnd), set_compare(rnd), set_words(rnd)]
    for s in sets:
        assert len(s["items"]) == 20, (s["title"], len(s["items"]))
        cnt = [0, 0, 0, 0]
        for it in s["items"]:
            assert len(set(it["c"])) == 4, it
            cnt[it["a"]] += 1
        assert cnt == [5, 5, 5, 5], (s["title"], cnt)
    return {
        "country": "ca-on", "subject": "math", "grade": "grade-2", "slug": "fractions-and-fair-shares", "sort": 7,
        "updated": UPDATED, "pdf_url": "",
        "title": "Grade 2 Fractions and Fair Shares",
        "seo_title": "Grade 2 Fractions and Fair Shares Worksheets: Free Math Practice with Answer Key (Ontario Curriculum)",
        "short_title": "Fractions and Fair Shares",
        "domain": "Number",
        "standard_code": "Grade 2: B1.6",
        "standard_url": "https://www.dcp.edu.gov.on.ca/en/curriculum/elementary-mathematics",
        "standard_text": "Use drawings to represent, solve, and compare the results of fair-share problems that involve sharing up to 10 items among 2, 3, 4, and 6 sharers, including problems that result in whole numbers, mixed numbers, and fractional amounts",
        "meta_desc": "Free Grade 2 math worksheets on fractions and fair shares for the Ontario curriculum: halves, thirds, fourths and sixths, sharing up to 10 items fairly, comparing shares and one third = two sixths. 100 questions with an answer key.",
        "key_big": "Fair shares are equal shares. More sharers means smaller shares.",
        "key_sub": "5 sandwiches shared by 2 friends: 2 each, then cut the last one in half. Each friend gets 2 and a half. One third is the same as two sixths.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, "fractions-and-fair-shares.json")
    mark_large(u, "(two bars|shared items|four pictures|four plate|plates of|[0-9]+ (cookie|apple)s)")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(u, f, ensure_ascii=False, indent=1)
    print("wrote", path)
