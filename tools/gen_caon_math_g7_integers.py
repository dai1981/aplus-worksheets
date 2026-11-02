# -*- coding: utf-8 -*-
"""
Ontario Grade 7 Math: Adding and Subtracting Integers (Ontario Mathematics Curriculum 2020, Grade 7: B2.4)
  python3 tools/gen_caon_math_g7_integers.py
Integer tiles and zero pairs (yellow = +1, red = −1), number lines with hops, adding integers with the same and
different signs, subtracting by adding the opposite (5 − (−3) = 5 + 3 = 8), and word problems in Ontario
contexts (temperatures in Thunder Bay, depths in the Great Lakes, the CN Tower, bank balances, parkade levels).
Wrong answers come from real student mistakes: −3 + 5 = −8 (adding the sizes and keeping a minus sign),
5 − (−3) = 2 (not changing the sign of the second number), giving the answer the sign of the wrong number,
ignoring every sign, moving the wrong way on the number line, counting the starting point as a step,
and |a| − |b| for the distance between a positive and a negative number.
Every answer is computed with Python integers. Helpers are adapted from gen_cabc_math_g7_add_sub_integers.py.
Canadian English, real minus sign −, brackets for negatives after an operator.
HTML attributes use single quotes (no backslashes in the JSON).
"""
import json, os, random, re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "ca-on", "math", "grade-7")
UPDATED = "2026-11-02"
GREEN = "#006633"
RED = "#c0392b"
INK = "#2b2b2b"
GRAY = "#8a8f8c"
YEL = "#f4c430"
TRED = "#d6453b"
FONT = "Arial, Helvetica, sans-serif"
M = "−"
NBSP = "\u00a0"
GIRLS = ["Olivia", "Emma", "Maya", "Zoe", "Amira", "Mei", "Chloe", "Priya", "Leah", "Hana", "Ava", "Sofia"]
BOYS = ["Liam", "Noah", "Aiden", "Lucas", "Owen", "Arjun", "Ethan", "Jayden", "Benjamin", "Mateo", "Nathan", "Kai"]


# ------------------------------------------------------------ numbers
def n(v):
    """Integer with the real minus sign. Ontario style: 4 digits with no separator, 5+ with a no-break space."""
    assert isinstance(v, int), v
    a = abs(v)
    s = str(a) if a < 10000 else "{:,}".format(a).replace(",", NBSP)
    return (M if v < 0 else "") + s


def b(v):
    """A number after an operator: negatives in brackets."""
    return "(" + n(v) + ")" if v < 0 else n(v)


def add(*vs):
    return n(vs[0]) + "".join(" + " + b(v) for v in vs[1:])


def sub(x, y):
    return n(x) + " " + M + " " + b(y)


def deg(v):
    return n(v) + NBSP + "°C"


def money(v):
    return (M if v < 0 else "") + "$" + n(abs(v))


def metres(v):
    return n(v) + NBSP + "m"


def sgn(v):
    return (v > 0) - (v < 0)


def plural(k, w):
    return "%d %s" % (k, w if k == 1 else w + "s")


# ------------------------------------------------------------ explanations
def add_rule(x, y):
    """Why x + y is what it is (two addends)."""
    r = x + y
    if x >= 0 and y >= 0:
        return "%s = <b>%s</b>." % (add(x, y), n(r))
    if x < 0 and y < 0:
        return ("Same signs: add the sizes, %d + %d = %d, and keep the negative sign. %s = <b>%s</b>."
                % (abs(x), abs(y), abs(r), add(x, y), n(r)))
    big = x if abs(x) > abs(y) else y
    word = "negative" if big < 0 else "positive"
    return ("Different signs: subtract the sizes, %d %s %d = %d. %s is farther from 0, so the answer is %s. "
            "%s = <b>%s</b>." % (max(abs(x), abs(y)), M, min(abs(x), abs(y)), abs(r), n(big), word, add(x, y), n(r)))


def sub_rule(x, y):
    """x − y by adding the opposite."""
    return "Add the opposite: %s = %s. " % (sub(x, y), add(x, -y)) + add_rule(x, -y)


# ------------------------------------------------------------ question helpers
def plain(s):
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", s)).strip()


def mcq(q, correct, cands, e):
    """correct and cands: strings, or (string, value) pairs. A candidate equal in value (or text) to the
    correct answer or to an earlier candidate is skipped. Positions are set later by balance()."""
    cs, cv = correct if isinstance(correct, tuple) else (correct, None)
    seen, vals, pick = {plain(cs)}, ({cv} if cv is not None else set()), []
    for c in cands:
        if c is None:
            continue
        s, v = c if isinstance(c, tuple) else (c, None)
        if not s or plain(s) in seen:
            continue
        if v is not None:
            if v in vals:
                continue
            vals.add(v)
        seen.add(plain(s))
        pick.append(s)
        if len(pick) == 3:
            break
    assert len(pick) == 3, (q, cs, cands)
    return {"q": q, "c": [cs] + pick, "a": 0, "e": e}


def mcq_v(q, v, cands, e, fmt=n):
    """Numeric answer; cands are int values (None skipped). Off-by-one values are added as a last resort."""
    extra = [v + 1, v - 1, v + 2, v - 2]
    return mcq(q, (fmt(v), v), [(fmt(c), c) for c in list(cands) + extra if c is not None], e)


def balance(sets, rnd):
    """Spread the correct answers evenly (5/5/5/5) over the 4 positions in every set."""
    for s in sets:
        targets = [0, 1, 2, 3] * 5
        rnd.shuffle(targets)
        for it, t in zip(s["items"], targets):
            c = it["c"]
            right = c[it["a"]]
            wrong = [x for i, x in enumerate(c) if i != it["a"]]
            rnd.shuffle(wrong)
            it["c"] = wrong[:t] + [right] + wrong[t:]
            it["a"] = t
        final = [sum(1 for it in s["items"] if it["a"] == i) for i in range(4)]
        assert final == [5, 5, 5, 5], (s["title"], final)


class People:
    def __init__(self, rnd):
        self.pool = [(x, "she", "her") for x in GIRLS] + [(x, "he", "his") for x in BOYS]
        rnd.shuffle(self.pool)
        self.i = 0

    def next(self):
        p = self.pool[self.i % len(self.pool)]
        self.i += 1
        return p


def fig(svg):
    return "<div class='qfig'>" + svg + "</div>"


def svg_wrap(w, h, body, label):
    return ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 %d %d' width='%d' height='%d' "
            "role='img' aria-label='%s'><g font-family='%s'>%s</g></svg>" % (w, h, w, h, label, FONT, body))


def text(x, y, t, fs=14, anchor="middle", bold=False, col=INK):
    return ("<text x='%.1f' y='%.1f' font-size='%d'%s fill='%s' text-anchor='%s'>%s</text>"
            % (x, y, fs, " font-weight='700'" if bold else "", col, anchor, t))


def tw(t, fs):
    return len(str(t)) * fs * 0.6


def table(head, rows):
    h = "".join("<th>%s</th>" % x for x in head)
    bd = "".join("<tr>" + "".join("<td>%s</td>" % c for c in r) + "</tr>" for r in rows)
    return "<div class='sn-tw'><table class='sn-table'><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>" % (h, bd)


def ex(title, q, s, a):
    return ("<div class='sn-ex'><span class='sn-ex-t'>%s</span><p class='sn-ex-q'>%s</p>"
            "<p class='sn-ex-s'>%s</p><p class='sn-ex-a'>Answer: %s</p></div>" % (title, q, s, a))


def mark_large(u, pattern):
    """Tag wide pictures (number lines, rows of tiles) so they print larger."""
    rx = re.compile(r"<svg (?=[^>]*aria-label='" + pattern + ")")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u


# ------------------------------------------------------------ pictures: integer tiles
T = 26          # tile size
P_ = 32         # tile pitch


def tile(x, y, pos):
    col = YEL if pos else TRED
    fg = INK if pos else "#ffffff"
    sym = "+" if pos else M
    return ("<rect x='%.1f' y='%.1f' width='%d' height='%d' rx='4' fill='%s' stroke='%s' stroke-width='1.4'/>"
            % (x, y, T, T, col, INK, ) + text(x + T / 2, y + T / 2 + 6.5, sym, 19, bold=True, col=fg))


def tiles_rows_svg(p, q, pairs=False):
    """p yellow (+1) tiles in the top row, q red (−1) tiles in the bottom row, lined up from the left.
    pairs: draw a dashed loop around each zero pair."""
    k = max(p, q)
    assert 1 <= k <= 10
    pad = 8
    W = int(2 * pad + k * P_ - (P_ - T))
    rows = [r for r in (p, q) if r]
    H = int(2 * pad + len(rows) * P_ - (P_ - T))
    s = []
    y = pad
    if p:
        for i in range(p):
            s.append(tile(pad + i * P_, y, True))
        y += P_
    if q:
        for i in range(q):
            s.append(tile(pad + i * P_, y, False))
    if pairs and p and q:
        for i in range(min(p, q)):
            s.append("<rect x='%.1f' y='%.1f' width='%d' height='%d' rx='8' fill='none' stroke='%s' "
                     "stroke-width='2' stroke-dasharray='4 3'/>" % (pad + i * P_ - 2, pad - 3, T + 4, P_ + T + 6, GREEN))
        W, H = W + 6, H + 6
        s = ["<g transform='translate(3 3)'>"] + s + ["</g>"]
    lab = "integer tiles: %s and %s" % (plural(p, "yellow tile"), plural(q, "red tile"))
    if pairs:
        lab += " with the zero pairs circled"
    return svg_wrap(W, H, "".join(s), lab)


def group_body(v, x0, y0, cols):
    s = []
    for i in range(abs(v)):
        s.append(tile(x0 + (i % cols) * P_, y0 + (i // cols) * P_, v > 0))
    return s


def tiles_groups_svg(x, y):
    """Two groups of tiles with a + sign between them: x then y."""
    cols = 5
    pad = 8

    def size(v):
        c = min(abs(v), cols)
        r = (abs(v) + cols - 1) // cols
        return c * P_ - (P_ - T), r * P_ - (P_ - T)
    w1, h1 = size(x)
    w2, h2 = size(y)
    H = int(max(h1, h2) + 2 * pad)
    s = group_body(x, pad, pad, cols)
    px = pad + w1 + 22
    s.append(text(px, H / 2 + 9, "+", 26, bold=True, col=GREEN))
    s += group_body(y, px + 22, pad, cols)
    W = int(px + 22 + w2 + pad)
    lab = "integer tiles: a group of %s, a plus sign, and a group of %s" % (
        plural(abs(x), "yellow tile" if x > 0 else "red tile"), plural(abs(y), "yellow tile" if y > 0 else "red tile"))
    return svg_wrap(W, H, "".join(s), lab)


# ------------------------------------------------------------ pictures: number lines
class NL:
    """Horizontal number line from lo to hi, a tick at every integer. Labels on every integer, or on every
    second one when the gap is too narrow. Dots and one-step hops (arcs) above the line."""

    def __init__(self, lo, hi, gap=None):
        self.lo, self.hi = lo, hi
        self.n = hi - lo
        lw = max(tw(n(v), 14) for v in range(lo, hi + 1))
        self.g = gap or max(30, int(lw + 7))
        self.lab = 1
        assert self.lab * self.g >= lw + 6, ("labels overlap", lo, hi)
        self.pad = int(max(26, lw / 2 + 8))
        self.W = int(2 * self.pad + self.n * self.g)
        self.pts, self.hops, self.hop_label = [], [], None

    def X(self, v):
        return self.pad + (v - self.lo) * self.g

    def point(self, v, name=None, col=GREEN):
        assert self.lo <= v <= self.hi
        self.pts.append((v, name, col))
        return self

    def hop(self, a, z, label=None):
        d = 1 if z > a else -1
        v = a
        while v != z:
            self.hops.append((v, v + d))
            v += d
        self.hop_label = label
        return self

    def svg(self, label):
        top = 0
        if self.hops:
            top = 30 + (20 if self.hop_label else 0)
        elif any(nm for _, nm, _ in self.pts):
            top = 14
        Y = 22 + top
        H = Y + 34
        s = []
        x0, x1 = self.pad - 16, self.W - self.pad + 16
        s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='2'/>" % (x0, Y, x1, Y, INK))
        s.append("<path d='M%d %d l9 -5 v10 z M%d %d l-9 -5 v10 z' fill='%s'/>" % (x0 - 2, Y, x1 + 2, Y, INK))
        for v in range(self.lo, self.hi + 1):
            x = self.X(v)
            big = v % self.lab == 0
            h = 8 if big else 5
            s.append("<line x1='%.1f' y1='%d' x2='%.1f' y2='%d' stroke='%s' stroke-width='%s'/>"
                     % (x, Y - h, x, Y + h, INK, "1.8" if big else "1.2"))
            if big:
                s.append(text(x, Y + 26, n(v), 14, bold=(v == 0)))
        for a, z in self.hops:
            xa, xb = self.X(a), self.X(z)
            s.append("<path d='M%.1f %d Q%.1f %d %.1f %d' fill='none' stroke='%s' stroke-width='1.8'/>"
                     % (xa, Y - 7, (xa + xb) / 2, Y - 30, xb, Y - 7, RED))
            dx = 1 if xb > xa else -1
            s.append("<path d='M%.1f %d L%.1f %d L%.1f %d z' fill='%s'/>"
                     % (xb, Y - 7, xb - dx * 8, Y - 11, xb - dx * 3, Y - 15, RED))
        if self.hops and self.hop_label:
            xs = [self.X(a) for a, z in self.hops] + [self.X(z) for a, z in self.hops]
            s.append(text((min(xs) + max(xs)) / 2, Y - 36, self.hop_label, 15, bold=True, col=RED))
        for v, nm, col in self.pts:
            x = self.X(v)
            s.append("<circle cx='%.1f' cy='%d' r='6' fill='%s'/>" % (x, Y, col))
            if nm:
                s.append(text(x, Y - 13, nm, 15, bold=True, col=col))
        return svg_wrap(self.W, H, "".join(s), label)


def nl_range(*vals):
    lo = min(min(vals), 0) - 1
    hi = max(max(vals), 0) + 1
    return lo, hi


# ------------------------------------------------------------ typical wrong answers
def add_cands(*vs):
    """Wrong sums from real mistakes, most likely first."""
    r = sum(vs)
    sizes = sum(abs(v) for v in vs)
    c = []
    if any(v < 0 for v in vs) and any(v > 0 for v in vs):
        c.append(-sizes)                      # −3 + 5 = −8: add the sizes, keep a minus sign
        c.append(-r)                          # sign of the wrong number
        c.append(sizes)                       # ignore every sign
    else:
        c.append(-r)                          # (−7) + (−5) = 12: lose the sign
        if len(vs) == 2:
            c.append(vs[0] - vs[1])           # subtract the sizes: −7 + (−5) = −2
            c.append(vs[1] - vs[0])
    if len(vs) == 3:
        c.append(vs[0] + vs[1] - vs[2])       # last sign changed
        c.append(vs[0] - vs[1] + vs[2])
    return c


def sub_cands(x, y):
    r = x - y
    return [x + y,                            # 5 − (−3) = 2: second sign not changed
            -r,                               # sign of the wrong number / order swapped
            -(x + y),
            abs(x) + abs(y), -(abs(x) + abs(y)), abs(x) - abs(y), abs(y) - abs(x)]



# ============================================================ set 1: integer tiles and zero pairs
def set_tiles(rnd, P):
    its = []
    # A: what integer do the tiles show? (5)
    for p, q in [(6, 2), (3, 7), (8, 3), (2, 9), (5, 10)]:
        r = p - q
        e = ("Each yellow and red pair is a zero pair: 1 + (%s1) = 0. There are %d zero pairs. "
             "Remove them: %s left. The tiles show <b>%s</b>."
             % (M, min(p, q), plural(abs(r), "yellow tile") + (" is" if abs(r) == 1 else " are") if r > 0
                else plural(abs(r), "red tile") + (" is" if abs(r) == 1 else " are"), n(r)))
        its.append(mcq_v(fig(tiles_rows_svg(p, q)) + "<p>A yellow tile is +1 and a red tile is " + M +
                         "1. What integer do these tiles show?</p>", r, [-r, p + q, p if r < 0 else -q, -(p + q)], e))
    # B: how many zero pairs? (3)
    for p, q in [(7, 4), (2, 6), (9, 5)]:
        k = min(p, q)
        e = ("A zero pair is 1 yellow tile and 1 red tile. There are only %d %s tiles, so you can make <b>%d zero pairs</b>."
             % (k, "yellow" if p < q else "red", k))
        fmt = lambda v: plural(v, "zero pair")
        its.append(mcq_v(fig(tiles_rows_svg(p, q)) + "<p>How many zero pairs can you make with these tiles?</p>",
                         k, [p + q, max(p, q), abs(p - q), 2 * k], e, fmt=fmt))
    # C: what is left after the zero pairs are removed? (3)
    for p, q in [(8, 3), (3, 9), (5, 7)]:
        k, r = min(p, q), p - q
        big = "yellow" if r > 0 else "red"
        other = "red" if r > 0 else "yellow"
        e = ("Remove %d zero pairs. There are more %s tiles, so %d %s tiles are left (%d %s %d = %d). "
             "They show %s." % (k, big, abs(r), big, max(p, q), M, k, abs(r), n(r)))
        its.append(mcq(fig(tiles_rows_svg(p, q)) + "<p>You remove all the zero pairs. What is left?</p>",
                       "%d %s tiles" % (abs(r), big),
                       ["%d %s tiles" % (abs(r), other), "%d %s tiles" % (p + q, big), "%d %s tiles" % (k, big),
                        "%d %s tiles" % (max(p, q), big)], e))
    # D: which addition do the tiles show? (2)
    for x, y in [(-5, 2), (7, -3)]:
        e = ("The first group has %s, so it is %s. The second group has %s, so it is %s. The tiles show <b>%s</b>."
             % (plural(abs(x), "yellow tile" if x > 0 else "red tile"), n(x),
                plural(abs(y), "yellow tile" if y > 0 else "red tile"), n(y), add(x, y)))
        its.append(mcq(fig(tiles_groups_svg(x, y)) + "<p>Which addition do these tiles show?</p>",
                       add(x, y), [add(-x, -y), add(x, -y), add(-x, y)], e))
    # E: the sum of the tiles (5)
    for x, y in [(-7, 3), (4, -9), (-2, -5), (8, -3), (-6, 6)]:
        nm, he, his = P.next()
        if sgn(x) != sgn(y):
            k = min(abs(x), abs(y))
            left = abs(x + y)
            if left == 0:
                e = ("Make %d zero pairs and remove them. No tiles are left, so the sum is <b>0</b>. "
                     "A number plus its opposite is always 0." % k)
            else:
                e = "Make %d zero pairs and remove them. %d %s tile%s left. " % (
                    k, left, "yellow" if x + y > 0 else "red", " is" if left == 1 else "s are") + add_rule(x, y)
        else:
            e = "All the tiles are red, so there are no zero pairs. Count them: %d red tiles. %s = <b>%s</b>." % (
                abs(x + y), add(x, y), n(x + y))
        cands = [-12, 12, 6] if x + y == 0 else add_cands(x, y)   # −6 + 6: add the sizes, or count one group
        its.append(mcq_v(fig(tiles_groups_svg(x, y)) + "<p>%s models %s with tiles. What is the sum?</p>" % (nm, add(x, y)),
                         x + y, cands, e))
    # F: reasoning with tiles (2)
    nm, he, his = P.next()
    e = ("The 6 red tiles show %s6. Each yellow tile you add makes a zero pair with a red tile and raises the value by 1. "
         "To get to %s2, add <b>4 yellow tiles</b>: %s = %s2." % (M, M, add(-6, 4), M))
    its.append(mcq_v("<p>%s wants to show %s2 with integer tiles. %s starts with 6 red tiles. How many yellow tiles does %s need to add?</p>"
                     % (nm, M, he.capitalize(), he), 4, [8, 2, 6], e, fmt=lambda v: plural(v, "yellow tile")))
    nm, he, his = P.next()
    e = ("3 zero pairs are worth 0. The other 8 red tiles are worth %s8. So 3 yellow tiles and 11 red tiles show "
         "%s = <b>%s</b>." % (M, add(3, -11), n(-8)))
    its.append(mcq_v("<p>%s shows an integer with 3 yellow tiles and 11 red tiles. What integer is it?</p>" % nm,
                     -8, [14, 8, -14, -3], e))
    return {"title": "Integer tiles and zero pairs", "items": its}


# ============================================================ set 2: number lines
def set_lines(rnd, P):
    its = []
    # A: which addition does the number line show? (6)
    for x, y in [(-5, 8), (4, -6), (-3, -4), (7, -10), (-6, 3), (-2, 9)]:
        z = x + y
        lo, hi = nl_range(x, z)
        nl = NL(lo, hi).point(x).hop(x, z)
        svg = nl.svg("number line from %s to %s with %d hops from %s to %s" % (n(lo), n(hi), abs(y), n(x), n(z)))
        e = ("The hops start at %s. There are %d hops to the %s, so you add %s. They end at %s: <b>%s = %s</b>."
             % (n(x), abs(y), "right" if y > 0 else "left", n(y), n(z), add(x, y), n(z)))
        its.append(mcq(fig(svg) + "<p>Which number sentence does the number line show?</p>",
                       "%s = %s" % (add(x, y), n(z)),
                       ["%s = %s" % (add(x, -y), n(x - y)), "%s = %s" % (add(z, y), n(z + y)),
                        "%s = %s" % (add(x, z), n(x + z)), "%s = %s" % (add(-x, y), n(-x + y))], e))
    # B: use the number line to add (8)
    for x, y in [(-6, 9), (3, -7), (-4, -3), (5, -8), (-9, 4), (-7, 10), (2, -9), (-1, -8)]:
        z = x + y
        lo, hi = nl_range(x, z)
        nl = NL(lo, hi).point(x)
        svg = nl.svg("number line from %s to %s with a dot at %s" % (n(lo), n(hi), n(x)))
        d = "right" if y > 0 else "left"
        e = "Start at the dot, %s. Adding %s means %d hops to the %s. You land on <b>%s</b>." % (n(x), n(y), abs(y), d, n(z))
        cands = [x - y, z - sgn(y)]
        if sgn(x) * sgn(z) < 0:
            cands.append(z + sgn(y))          # skipped 0
        its.append(mcq_v(fig(svg) + "<p>Start at the dot. Use the number line to find %s.</p>" % add(x, y),
                         z, cands + add_cands(x, y), e))
    # C: use the number line to subtract (6)
    for x, y in [(4, 7), (-3, 5), (2, -6), (-7, -9), (5, 8), (-4, -7)]:
        z = x - y
        lo, hi = nl_range(x, z)
        nl = NL(lo, hi).point(x)
        svg = nl.svg("number line from %s to %s with a dot at %s" % (n(lo), n(hi), n(x)))
        if y > 0:
            e = "Subtracting %d means %d hops to the left. Start at %s and you land on <b>%s</b>." % (y, y, n(x), n(z))
        else:
            e = ("Subtracting %s is the same as adding %d: %s = %s. Make %d hops to the right from %s. You land on <b>%s</b>."
                 % (n(y), -y, sub(x, y), add(x, -y), -y, n(x), n(z)))
        its.append(mcq_v(fig(svg) + "<p>Start at the dot. Use the number line to find %s.</p>" % sub(x, y),
                         z, [x + y, z + sgn(y)] + sub_cands(x, y), e))
    return {"title": "Number lines", "items": its}


# ============================================================ set 3: adding integers
def set_adding(rnd, P):
    its = []
    plan = [(-4, -6), (-7, -3), (-5, -8), (-9, -6),                      # same signs
            (-4, 7), (8, -3), (-10, 6), (3, -9), (-6, 11), (7, -12),     # different signs
            (-28, 19), (43, -67), (-35, -48), (-57, 72)]                 # two-digit
    for x, y in plan:
        its.append(mcq_v("<p>What is %s?</p>" % add(x, y), x + y, add_cands(x, y), add_rule(x, y)))
    # sign reasoning (2)
    q = "<p>Without calculating, what can you say about %s?</p>" % add(-53, 38)
    e = ("The signs are different, so the sum has the sign of the number farther from 0. 53 &gt; 38, "
         "so the sum is negative (it is %s)." % n(-15))
    its.append(mcq(q, "It is negative, because " + M + "53 is farther from 0.",
                   ["It is positive, because 38 is positive.", "It is negative, because both numbers are negative.",
                    "It is positive, because 53 + 38 is positive."], e))
    q = "<p>Without calculating, what can you say about %s?</p>" % add(-26, 71)
    e = ("The signs are different, so the sum has the sign of the number farther from 0. 71 &gt; 26, "
         "so the sum is positive (it is 45).")
    its.append(mcq(q, "It is positive, because 71 is farther from 0.",
                   ["It is negative, because " + M + "26 comes first.", "It is negative, because 26 + 71 is 97.",
                    "It is 0, because the signs are different."], e))
    # three addends (4)
    for vs in [(-9, 16, -8), (14, -6, -11), (-5, -9, 22), (-150, 275, -90)]:
        r = sum(vs)
        pos = sum(v for v in vs if v > 0)
        neg = sum(v for v in vs if v < 0)
        e = ("Add the positives and the negatives separately: %s and %s. Then %s = <b>%s</b>."
             % (n(pos), n(neg), add(pos, neg), n(r)))
        its.append(mcq_v("<p>What is %s?</p>" % add(*vs), r, add_cands(*vs), e))
    assert len(its) == 20
    return {"title": "Adding integers", "items": its}


# ============================================================ set 4: subtracting integers
def set_subtracting(rnd, P):
    its = []
    # which addition has the same answer? (4)
    for x, y in [(6, -4), (-5, 7), (-3, -8), (9, 12)]:
        e = "To subtract, add the opposite. The opposite of %s is %s, so %s = <b>%s</b>." % (n(y), n(-y), sub(x, y), add(x, -y))
        its.append(mcq("<p>Which addition has the same answer as %s?</p>" % sub(x, y), add(x, -y),
                       [add(x, y), add(-x, -y), add(-x, y)], e))
    plan = [(4, 9), (3, 12), (7, -2), (-5, -11), (-9, -4), (-3, 8), (-8, 6), (8, -5), (-2, -12), (10, 16),
            (-30, -45), (18, 56)]
    for x, y in plan:
        its.append(mcq_v("<p>What is %s?</p>" % sub(x, y), x - y, sub_cands(x, y), sub_rule(x, y)))
    # three terms (4)
    for x, y, z in [(-4, 6, -11), (5, -7, 8), (-13, -9, 6), (12, 14, -25)]:
        r = x - y - z
        e = ("Add the opposite of each number you subtract: %s %s %s = %s = <b>%s</b>."
             % (sub(x, y), M, b(z), add(x, -y, -z), n(r)))
        cands = [x + y + z, x - y + z, x + y - z, -r]
        its.append(mcq_v("<p>What is %s %s %s?</p>" % (sub(x, y), M, b(z)), r, cands, e))
    assert len(its) == 20
    return {"title": "Subtracting integers: add the opposite", "items": its}


# ============================================================ set 5: word problems
def set_words(rnd, P):
    its = []

    def mq(q, v, cands, e, fmt=n):
        its.append(mcq_v("<p>" + q + "</p>", v, cands, e, fmt=fmt))

    deg_n = lambda v: plural(v, "degree")
    m_ = lambda v: n(v) + NBSP + "m"
    # 1 Thunder Bay morning warms up
    mq("At 7 a.m. on a January day in Thunder Bay, the temperature was %s. By noon it had risen 13 degrees. "
       "What was the temperature at noon?" % deg(-21),
       -8, [-34, 8, -9], "Rising means adding: %s = <b>%s</b>." % (add(-21, 13), deg(-8)), fmt=deg)
    # 2 Sudbury evening falls
    mq("In Sudbury, it was %s at 5 p.m. The temperature fell 11 degrees by midnight. What was the temperature at midnight?" % deg(5),
       -6, [16, 6, -5], "Falling means subtracting: %s = %s = <b>%s</b>." % (sub(5, 11), add(5, -11), deg(-6)), fmt=deg)
    # 3 Toronto vs Thunder Bay
    mq("On the same winter morning, it was %s in Toronto and %s in Thunder Bay. How many degrees warmer was Toronto?"
       % (deg(4), deg(-17)),
       21, [13, 17, 4], "Find the difference: %s = %s = <b>21 degrees</b>. On a number line, 4 to 0 is 4 and 0 to %s is 17: 4 + 17 = 21."
       % (sub(4, -17), add(4, 17), n(-17)), fmt=deg_n)
    # 4 ski hill
    mq("At the bottom of a ski hill near Collingwood, the temperature is %s. At the top it is 3 degrees colder. "
       "What is the temperature at the top?" % deg(-5),
       -8, [-2, 2, 8], "Colder means subtracting: %s = %s = <b>%s</b>." % (sub(-5, 3), add(-5, -3), deg(-8)), fmt=deg)
    # 5 Thunder Bay rise during the day
    mq("In Thunder Bay, the temperature was %s at 7 a.m. and %s at 3 p.m. How many degrees did the temperature rise?"
       % (deg(-14), deg(3)),
       17, [11, 14, 3], "Rise = later temperature " + M + " earlier temperature: %s = %s = <b>17 degrees</b>."
       % (sub(3, -14), add(3, 14)), fmt=deg_n)
    # 6 bakery profit and loss
    mq("A bakery in Hamilton had a loss of $12" + NBSP + "500 in its first year, written as " + money(-12500) + ". It had a profit of "
       "$18" + NBSP + "200 in its second year. What is the total for the two years?",
       5700, [-30700, 30700, -5700], "Add the two results: %s = <b>$5700</b>. The profit is farther from 0, so the total is positive."
       % add(-12500, 18200), fmt=money)
    # 7 diver swims up (Tobermory shipwrecks)
    nm, he, his = P.next()
    mq("%s is scuba diving near Tobermory at %s. %s swims up 6" % (nm, metres(-15), he.capitalize()) + NBSP +
       "m. What is %s new position?" % his,
       -9, [-21, 9, 21], "Up means adding: %s = <b>%s</b>. %s is still below the surface." % (add(-15, 6), metres(-9), he.capitalize()),
       fmt=metres)
    # 8 diver goes down to a shipwreck
    nm, he, his = P.next()
    mq("%s is diving at %s in Lake Huron. %s goes down another 8" % (nm, metres(-10), he.capitalize()) + NBSP +
       "m to look at a shipwreck. What is %s new position?" % his,
       -18, [-2, 2, 18], "Down means subtracting: %s = %s = <b>%s</b>." % (sub(-10, 8), add(-10, -8), metres(-18)), fmt=metres)
    # 9 two divers apart
    a, b2 = P.next(), P.next()
    mq("%s is diving at %s and %s is diving at %s. How far apart are they?" % (a[0], metres(-7), b2[0], metres(-19)),
       12, [26, 19, 7], "Subtract the positions: %s = %s = <b>12" % (sub(-7, -19), add(-7, 19)) + NBSP +
       "m</b>. Both are below the surface, so the distance is 19 " + M + " 7.", fmt=m_)
    # 10 CN Tower and a subway tunnel
    mq("The CN Tower in Toronto is 553" + NBSP + "m tall. Ground level is 0" + NBSP + "m, and a subway tunnel nearby is at %s. "
       "How much higher is the top of the CN Tower than the tunnel?" % metres(-20),
       573, [533, 553, 20], "%s = %s = <b>573" % (sub(553, -20), add(553, 20)) + NBSP + "m</b>. Count 20" + NBSP +
       "m up to ground level, then 553" + NBSP + "m more.", fmt=m_)
    # 11 Lake Superior
    mq("The surface of Lake Superior is about 183" + NBSP + "m above sea level. Its deepest point is 406" + NBSP +
       "m below the surface. What is the elevation of the deepest point compared with sea level?",
       -223, [589, 223, -589], "Start at 183 and go down 406: %s = %s = <b>%s</b>. The deepest point is below sea level."
       % (sub(183, 406), add(183, -406), metres(-223)), fmt=metres)
    # 12 bank goes below zero
    nm, he, his = P.next()
    mq("%s has $35 in %s bank account. %s buys a $50 video game with %s debit card, and the account goes below zero. "
       "What is the balance now?" % (nm, his, he.capitalize(), his),
       -15, [15, -85, 85], "Spending means subtracting: %s = %s = <b>%s</b>. %s owes the bank $15."
       % (sub(35, 50), add(35, -50), money(-15), he.capitalize()), fmt=money)
    # 13 deposit after owing
    nm, he, his = P.next()
    mq("%s’s bank balance is %s. %s deposits $60 of birthday money. What is the balance now?" % (nm, money(-25), he.capitalize()),
       35, [-35, -85, 85], "A deposit means adding: %s = <b>$35</b>." % add(-25, 60), fmt=money)
    # 14 two steps bank
    nm, he, his = P.next()
    mq("%s’s balance is %s. %s deposits $30, then spends $20 at a sports store in Ottawa. What is the balance now?"
       % (nm, money(-18), he.capitalize()),
       -8, [-38, 8, 32], "%s = %s = <b>%s</b>." % (add(-18, 30, -20), add(12, -20), money(-8)), fmt=money)
    # 15 parkade levels
    nm, he, his = P.next()
    mq("In a Toronto parkade, the ground floor is level 0 and the levels below it are " + M + "1, " + M + "2, and so on. "
       "%s parks on level %s and takes the elevator up to level 2. How many levels does %s go up?" % (nm, n(-5), he),
       7, [3, 2, 5], "%s = %s = <b>7 levels</b>. Count 5 levels up to 0, then 2 more." % (sub(2, -5), add(2, 5)),
       fmt=lambda v: plural(v, "level"))
    # 16 elevator down
    nm, he, his = P.next()
    mq("%s gets on the elevator in a Mississauga building on level 6. %s goes down 9 levels to the parkade. "
       "Which level is %s on now?" % (nm, he.capitalize(), he),
       -3, [3, 15, -15], "Down means subtracting: %s = %s = <b>%s</b>." % (sub(6, 9), add(6, -9), n(-3)),
       fmt=lambda v: "level " + n(v))
    # 17 class quiz game
    mq("In a class quiz game, a right answer is +10 points and a wrong answer is " + M + "15 points. "
       "A team has %s points and then gets one wrong answer. What is the team’s score now?" % n(-25),
       -40, [-10, 40, 10], "A wrong answer adds " + M + "15: %s = <b>%s</b>." % (add(-25, -15), n(-40)),
       fmt=lambda v: n(v) + " points")
    # 18 hockey plus-minus
    nm, he, his = P.next()
    mq("In hockey, a player’s plus-minus goes up 1 when the player’s team scores while the player is on the ice, and down 1 "
       "when the other team scores. %s’s plus-minus is 2. In the next game, %s team scores 1 goal and the other team scores 4 "
       "while %s is on the ice. What is %s plus-minus now?" % (nm, his, he, his),
       -1, [7, 1, -3], "The change is %s = %s3. Then %s = <b>%s</b>." % (add(1, -4), M, add(2, -3), n(-1)))
    # 19 work backwards overnight
    mq("In Thunder Bay, the temperature dropped 14 degrees overnight. In the morning it was %s. "
       "What was the temperature the evening before?" % deg(-22),
       -8, [-36, 8, 36], "Work backwards: the evening was 14 degrees warmer. %s = <b>%s</b>." % (add(-22, 14), deg(-8)),
       fmt=deg)
    # 20 high and low of the week
    mq("In one week in Thunder Bay, the highest temperature was %s and the lowest was %s. "
       "What is the difference between the highest and lowest temperatures?" % (deg(6), deg(-27)),
       33, [21, 27, 6], "%s = %s = <b>33 degrees</b>. From %s up to 0 is 27 degrees, and 0 up to 6 is 6 more."
       % (sub(6, -27), add(6, 27), n(-27)), fmt=deg_n)
    assert len(its) == 20
    return {"title": "Word problems: temperatures, elevations and money", "items": its}


# ============================================================ lesson
def body_html():
    f_tiles = tiles_rows_svg(4, 6, pairs=True)
    nl1 = NL(-5, 4).point(-4).point(3).hop(-4, 3, "+7")
    f_add = nl1.svg("number line from " + M + "5 to 4 with 7 hops to the right from " + M + "4 to 3")
    nl2 = NL(-1, 9).point(5).point(8).hop(5, 8, "+3")
    f_sub = nl2.svg("number line from " + M + "1 to 9 with 3 hops to the right from 5 to 8")
    return (
        "<h2>Zero pairs</h2>"
        "<p>A yellow tile is +1 and a red tile is " + M + "1. One yellow tile and one red tile make a <b>zero pair</b>: "
        "1 + (" + M + "1) = 0. You can add or remove zero pairs without changing the value.</p>"
        "<figure class='sn-fig'>" + f_tiles +
        "<figcaption>" + add(4, -6) + ": make 4 zero pairs and remove them. 2 red tiles are left, so " + add(4, -6) +
        " = " + n(-2) + ".</figcaption></figure>"
        "<h2>Adding on a number line</h2>"
        "<p>Start at the first number. Adding a positive number moves <b>right</b>. Adding a negative number moves <b>left</b>.</p>"
        "<figure class='sn-fig'>" + f_add +
        "<figcaption>" + add(-4, 7) + ": start at " + n(-4) + " and make 7 hops to the right. You land on 3.</figcaption></figure>"
        "<h2>Rules for adding</h2>" +
        table(["Signs", "What to do", "Example"], [
            ["Same signs", "Add the sizes. Keep the sign.", add(-6, -5) + " = " + n(-11)],
            ["Different signs", "Subtract the sizes. Use the sign of the number farther from 0.", add(-3, 5) + " = 2"],
        ]) +
        ex("Example 1", "What is " + add(8, -13) + "?",
           "Different signs: 13 " + M + " 8 = 5. " + n(-13) + " is farther from 0, so the answer is negative.", n(-5)) +
        "<h2>Subtracting: add the opposite</h2>"
        "<p>To subtract an integer, <b>add its opposite</b>. Keep the first number, change " + M + " to +, "
        "and change the sign of the second number.</p>"
        "<figure class='sn-fig'>" + f_sub +
        "<figcaption>" + sub(5, -3) + " = " + add(5, 3) + " = 8. Taking away " + n(-3) + " moves right, like adding 3.</figcaption></figure>" +
        ex("Example 2", "What is " + sub(-6, 4) + "?",
           "Add the opposite: " + add(-6, -4) + ". Same signs: 6 + 4 = 10, keep the negative sign.", n(-10)) +
        ex("Example 3", "At 6 a.m. in Thunder Bay it was " + deg(-16) + ". At 2 p.m. it was " + deg(2) +
           ". How many degrees did the temperature rise?",
           "Later " + M + " earlier: " + sub(2, -16) + " = " + add(2, 16) + " = 18.", "18 degrees") +
        "<h2>Common mistakes</h2>" +
        table(["Mistake", "What to do instead"], [
            [add(-3, 5) + " = " + n(-8), "Different signs: subtract the sizes. " + add(-3, 5) + " = 2"],
            [sub(5, -3) + " = 2", "Add the opposite: " + add(5, 3) + " = 8"],
            [add(4, -9) + " = 5", "Use the sign of the number farther from 0: " + n(-5)],
            [add(-6, -2) + " = 8", "Same signs keep the sign: " + n(-8)],
            ["Counting the starting point as a hop", "Count the jumps, not the dots"],
        ])
    )


FAQ = [
    {"q": "How do you add and subtract integers in Grade 7?",
     "a": "To add, look at the signs: with the same signs, add and keep the sign; with different signs, subtract and use the sign of the number farther from 0. To subtract, add the opposite: 5 − (−3) = 5 + 3 = 8."},
    {"q": "Which Ontario Grade 7 expectation covers adding and subtracting integers?",
     "a": "Expectation B2.4 in the Number strand of the 2020 Ontario math curriculum: students use objects, diagrams and equations to add and subtract integers in real situations."},
    {"q": "What is a zero pair in math?",
     "a": "A zero pair is one positive tile and one negative tile, because +1 + (−1) = 0. Removing zero pairs does not change the value, so −7 + 3 leaves 4 red tiles, which is −4."},
    {"q": "Why does subtracting a negative number make the answer bigger?",
     "a": "Subtracting is the same as adding the opposite, so 5 − (−3) = 5 + 3 = 8. On a number line, 5 is 8 steps to the right of −3."},
]


def gen():
    rnd = random.Random(47805)
    P = People(rnd)
    sets = [set_tiles(rnd, P), set_lines(rnd, P), set_adding(rnd, P), set_subtracting(rnd, P), set_words(rnd, P)]
    balance(sets, rnd)
    seen = set()
    for s in sets:
        assert len(s["items"]) == 20, (s["title"], len(s["items"]))
        for it in s["items"]:
            assert len({plain(c) for c in it["c"]}) == 4, it
            assert it["e"], it
            assert it["q"].count("<svg") <= 1
            k = it["q"] + "|" + "|".join(sorted(it["c"]))
            assert k not in seen, it["q"]
            seen.add(k)
    u = {
        "country": "ca-on", "subject": "math", "grade": "grade-7", "slug": "adding-and-subtracting-integers", "sort": 5,
        "updated": UPDATED, "pdf_url": "",
        "title": "Grade 7 Adding and Subtracting Integers",
        "seo_title": "Grade 7 Adding and Subtracting Integers Worksheets: Free Math Practice with Answer Key (Ontario Curriculum)",
        "short_title": "Adding and subtracting integers",
        "domain": "Number",
        "standard_code": "Grade 7: B2.4",
        "standard_url": "https://www.dcp.edu.gov.on.ca/en/curriculum/elementary-mathematics",
        "standard_text": "Use objects, diagrams, and equations to represent, describe, and solve situations involving addition and subtraction of integers",
        "meta_desc": "Free Grade 7 math worksheets on adding and subtracting integers for the Ontario curriculum: integer tiles and zero pairs, number lines, adding integers, subtracting by adding the opposite, and word problems with temperatures, elevations and bank balances. 100 questions with an answer key.",
        "key_big": "To subtract an integer, add its opposite: 5 − (−3) = 5 + 3 = 8.",
        "key_sub": "Same signs: add and keep the sign, so −6 + (−5) = −11. Different signs: subtract and use the sign of the number farther from 0, so −3 + 5 = 2, not −8.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }
    return mark_large(u, "(number line|integer tiles)")


if __name__ == "__main__":
    u = gen()
    for st in u["sets"]:          # question text plain like other units (a <p> renders it small)
        for it in st["items"]:
            it["q"] = it["q"].replace("<p>", "").replace("</p>", "")
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
