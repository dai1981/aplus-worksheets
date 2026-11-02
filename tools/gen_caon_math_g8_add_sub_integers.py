# -*- coding: utf-8 -*-
"""
Ontario Grade 8 Math: Adding and Subtracting Integers (Ontario Curriculum 2020, B2.4)
  python3 tools/gen_caon_math_g8_add_sub_integers.py
Review with integer tiles (zero pairs) and number lines, sums with larger values (to 5 digits),
subtracting by adding the opposite, multi-term expressions such as -7 + 12 - (-5) and expressions with
brackets, and word problems (Thunder Bay temperatures, golf scores, bank balances, elevations).
Wrong answers come from real student mistakes: 12 - (-5) = 7 (sign of the subtracted negative not changed),
+ (-5) read as +5, adding the sizes and keeping a minus sign, the sign of the wrong number, ignoring signs,
|a| - |b| for the distance across 0, and removing brackets without changing signs.
Helpers adapted from gen_cabc_math_g7_add_sub_integers.py. Every answer is computed with Python integers.
Canadian English, real minus sign, no-break space in 5+ digit numbers, single-quoted HTML attributes.
"""
import json, os, random, re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "ca-on", "math", "grade-8")
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
        return ("Same signs: add the sizes, %s + %s = %s, and keep the negative sign. %s = <b>%s</b>."
                % (n(abs(x)), n(abs(y)), n(abs(r)), add(x, y), n(r)))
    big = x if abs(x) > abs(y) else y
    word = "negative" if big < 0 else "positive"
    return ("Different signs: subtract the sizes, %s %s %s = %s. %s is farther from 0, so the answer is %s. "
            "%s = <b>%s</b>." % (n(max(abs(x), abs(y))), M, n(min(abs(x), abs(y))), n(abs(r)), n(big), word, add(x, y), n(r)))


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



# ------------------------------------------------------------ multi-term expressions
# An expression is a list of (op, value): the first op is "+", later ops are "+" or "−".
def ex_text(terms):
    s = n(terms[0][1])
    for op, v in terms[1:]:
        s += (" + " if op == "+" else " " + M + " ") + b(v)
    return s


def ex_val(terms):
    return sum(v if op == "+" else -v for op, v in terms)


def ex_opp(terms):
    """Every subtraction rewritten as adding the opposite."""
    return add(*[v if op == "+" else -v for op, v in terms])


def ex_rule(terms):
    vs = [v if op == "+" else -v for op, v in terms]
    r = sum(vs)
    pos = sum(v for v in vs if v > 0)
    neg = sum(v for v in vs if v < 0)
    s = ""
    if any(op != "+" for op, _ in terms):
        s = "Add the opposite: %s. " % add(*vs)
    if pos and neg:
        s += "Positives: %s. Negatives: %s. %s = <b>%s</b>." % (n(pos), n(neg), add(pos, neg), n(r))
    else:
        s += "All the numbers have the same sign, so add the sizes and keep the sign: <b>%s</b>." % n(r)
    return s


def ex_cands(terms):
    """Wrong values from real mistakes."""
    r = ex_val(terms)
    first = terms[0][1]
    c = []
    # 12 − (−5) read as 12 − 5: the sign of a negative being subtracted is not changed
    c.append(first + sum((v if op == "+" else -abs(v)) for op, v in terms[1:]))
    # + (−5) read as +5 ("two signs make a plus")
    c.append(first + sum((abs(v) if op == "+" else -v) for op, v in terms[1:]))
    # − changed to + but the sign of the number kept
    c.append(first + sum(v for op, v in terms[1:]))
    c.append(-r)
    # every sign ignored
    c.append(abs(first) + sum((abs(v) if op == "+" else -abs(v)) for op, v in terms[1:]))
    # last operation done the wrong way
    op, v = terms[-1]
    c.append(r - 2 * v if op == "+" else r + 2 * v)
    return [x for x in c if x != r]


def signed(v):
    return ("+" if v > 0 else "") + n(v)


# ============================================================ set 1: review
def set_review(rnd, P):
    its = []
    # A: what integer do the tiles show? (3)
    for p, q in [(6, 2), (3, 8), (4, 9)]:
        r = p - q
        e = ("Each yellow and red pair is a zero pair: 1 + (%s1) = 0. Remove the %d zero pairs. "
             "%s left, so the tiles show <b>%s</b>."
             % (M, min(p, q), plural(abs(r), "yellow tile" if r > 0 else "red tile") + (" is" if abs(r) == 1 else " are"), n(r)))
        its.append(mcq_v(fig(tiles_rows_svg(p, q)) + "<p>Yellow tiles are +1 and red tiles are " + M +
                         "1. What integer do these tiles show?</p>", r, [-r, p + q, -(p + q)], e))
    # B: the sum shown by two groups of tiles (4)
    for x, y in [(-7, 3), (5, -9), (-4, -6), (8, -3)]:
        k = min(abs(x), abs(y)) if sgn(x) != sgn(y) else 0
        if k:
            left = abs(x + y)
            e = "Make %d zero pairs and remove them. %d %s tile%s left. " % (
                k, left, "yellow" if x + y > 0 else "red", " is" if left == 1 else "s are") + add_rule(x, y)
        else:
            e = "All the tiles are red, so there are no zero pairs. Count them: %d red tiles. %s = <b>%s</b>." % (
                abs(x + y), add(x, y), n(x + y))
        its.append(mcq_v(fig(tiles_groups_svg(x, y)) + "<p>What sum do these integer tiles show?</p>",
                         x + y, add_cands(x, y), e))
    # C: which number sentence does the number line show? (4)
    for x, y in [(-5, 8), (4, -7), (-2, -6), (-8, 3)]:
        z = x + y
        lo, hi = nl_range(x, z)
        svg = NL(lo, hi).point(x).hop(x, z).svg(
            "number line from %s to %s with %d hops from %s to %s" % (n(lo), n(hi), abs(y), n(x), n(z)))
        e = ("The hops start at %s. There are %d hops to the %s, so you add %s. They end at %s: <b>%s = %s</b>."
             % (n(x), abs(y), "right" if y > 0 else "left", n(y), n(z), add(x, y), n(z)))
        its.append(mcq(fig(svg) + "<p>Which number sentence does the number line show?</p>",
                       "%s = %s" % (add(x, y), n(z)),
                       ["%s = %s" % (add(x, -y), n(x - y)), "%s = %s" % (add(z, y), n(z + y)),
                        "%s = %s" % (add(-x, y), n(-x + y)), "%s = %s" % (add(x, z), n(x + z))], e))
    # D: add with a number line (4)
    for x, y in [(-6, 9), (3, -8), (-1, -7), (7, -10)]:
        z = x + y
        lo, hi = nl_range(x, z)
        svg = NL(lo, hi).point(x).svg("number line from %s to %s with a dot at %s" % (n(lo), n(hi), n(x)))
        e = "Start at the dot, %s. Adding %s means %d hops to the %s. You land on <b>%s</b>." % (
            n(x), n(y), abs(y), "right" if y > 0 else "left", n(z))
        cands = [x - y, z - sgn(y)]
        if sgn(x) * sgn(z) < 0:
            cands.append(z + sgn(y))
        its.append(mcq_v(fig(svg) + "<p>Start at the dot. Use the number line to find %s.</p>" % add(x, y),
                         z, cands + add_cands(x, y), e))
    # E: subtract with a number line (5)
    for x, y in [(2, 6), (-3, -7), (1, -6), (-4, 3), (-6, -2)]:
        z = x - y
        lo, hi = nl_range(x, z)
        svg = NL(lo, hi).point(x).svg("number line from %s to %s with a dot at %s" % (n(lo), n(hi), n(x)))
        if y > 0:
            e = "Subtracting %d means %d hops to the left. Start at %s and you land on <b>%s</b>." % (y, y, n(x), n(z))
        else:
            e = ("Subtracting %s is the same as adding %d: %s = %s. Make %d hops to the right from %s. You land on <b>%s</b>."
                 % (n(y), -y, sub(x, y), add(x, -y), -y, n(x), n(z)))
        its.append(mcq_v(fig(svg) + "<p>Start at the dot. Use the number line to find %s.</p>" % sub(x, y),
                         z, [x + y, z + sgn(y)] + sub_cands(x, y), e))
    assert len(its) == 20
    return {"title": "Number lines and zero pairs (review)", "items": its}


# ============================================================ set 2: adding with larger values
def set_adding(rnd, P):
    its = []
    plan = [(-36, -48), (-64, 29), (85, -132), (-150, 95), (-275, -160), (340, -415), (-508, 239),
            (-1250, 875), (2400, -3150), (-4800, -2750), (6350, -9875), (-12500, 9800), (18000, -25500)]
    for x, y in plan[:7]:
        its.append(mcq_v("<p>What is %s?</p>" % add(x, y), x + y, add_cands(x, y), add_rule(x, y)))
    # sign reasoning (2)
    q = "<p>Without calculating, what can you say about %s?</p>" % add(-386, 247)
    e = ("The signs are different, so the sum has the sign of the number farther from 0. 386 &gt; 247, "
         "so the sum is negative (it is %s)." % n(-139))
    its.append(mcq(q, "It is negative, because " + M + "386 is farther from 0.",
                   ["It is positive, because 247 is positive.", "It is negative, because both numbers are negative.",
                    "It is 0, because the signs are different."], e))
    q = "<p>Without calculating, what can you say about %s?</p>" % add(512, -497)
    e = ("The signs are different, so the sum has the sign of the number farther from 0. 512 &gt; 497, "
         "so the sum is positive (it is 15).")
    its.append(mcq(q, "It is positive, because 512 is farther from 0.",
                   ["It is negative, because " + M + "497 is negative.", "It is positive, because 512 + 497 = 1009.",
                    "It is negative, because 497 is close to 512."], e))
    for x, y in plan[7:]:
        its.append(mcq_v("<p>What is %s?</p>" % add(x, y), x + y, add_cands(x, y), add_rule(x, y)))
    # which sum is negative? (2)
    for i, (neg_, *others) in enumerate([((-91, 84), (63, -58), (-47, 120), (75, -38)),
                                         ((-305, 296), (-150, 210), (275, -240), (-99, 180))]):
        e = ("A sum of two numbers with different signs has the sign of the number farther from 0. In %s, "
             "%s is farther from 0, so the sum is negative: %s = <b>%s</b>." % (add(*neg_), n(neg_[0]), add(*neg_), n(sum(neg_))))
        its.append(mcq("<p>Which sum is negative?</p>", add(*neg_), [add(*o) for o in others], e))
    # missing addend (3)
    for a, r, first in [(-45, 18, True), (-72, -30, False), (125, -40, True)]:
        x = r - a
        if first:
            q = "<p>%s + ? = %s. What is the missing integer?</p>" % (n(a), n(r))
        else:
            q = "<p>? + %s = %s. What is the missing integer?</p>" % (b(a), n(r))
        e = "The missing integer is %s = %s = <b>%s</b>. Check: %s = %s." % (
            sub(r, a), add(r, -a), n(x), add(a, x) if first else add(x, a), n(r))
        its.append(mcq_v(q, x, [r + a, -x, -(r + a), abs(r) + abs(a)], e))
    assert len(its) == 20, len(its)
    return {"title": "Adding integers with larger values", "items": its}


# ============================================================ set 3: subtracting
def set_subtracting(rnd, P):
    its = []
    for x, y in [(9, -14), (-16, 7), (-23, -11)]:
        e = "To subtract, add the opposite. The opposite of %s is %s, so %s = <b>%s</b>." % (n(y), n(-y), sub(x, y), add(x, -y))
        its.append(mcq("<p>Which addition has the same value as %s?</p>" % sub(x, y), add(x, -y),
                       [add(x, y), add(-x, -y), add(-x, y)], e))
    plan = [(-14, 9), (23, -17), (-38, -52), (-45, -19), (60, 85), (-120, 75), (215, -190), (-340, -125),
            (1500, -2750), (-3200, 4600), (-15000, -8500)]
    for x, y in plan:
        its.append(mcq_v("<p>What is %s?</p>" % sub(x, y), x - y, sub_cands(x, y), sub_rule(x, y)))
    # find the error (3)
    for x, y, wrong in [(14, -9, 5), (-26, -40, -66), (-31, 18, -13)]:
        nm, he, his = P.next()
        r = x - y
        e = ("%s made a sign error. " % nm) + sub_rule(x, y)
        its.append(mcq_v("<p>%s wrote %s = %s. That is wrong. What is the correct answer?</p>"
                         % (nm, sub(x, y), n(wrong)), r, [wrong, -r, -wrong] + sub_cands(x, y), e))
    # distance between two integers (3)
    for x, y in [(-27, 45), (-63, -18), (-150, 85)]:
        hi_, lo_ = max(x, y), min(x, y)
        d = hi_ - lo_
        e = "Subtract the smaller integer from the greater one: %s = %s = <b>%d</b>." % (sub(hi_, lo_), add(hi_, -lo_), d)
        its.append(mcq_v("<p>How far apart are %s and %s on a number line?</p>" % (n(x), n(y)), d,
                         [abs(abs(x) - abs(y)), abs(x) + abs(y), -d, max(abs(x), abs(y))], e))
    assert len(its) == 20
    return {"title": "Subtracting integers: add the opposite", "items": its}


# ============================================================ set 4: multi-term expressions
def set_multi(rnd, P):
    its = []
    three = [
        [("+", -7), ("+", 12), ("−", -5)],
        [("+", 9), ("−", 15), ("+", -4)],
        [("+", -6), ("−", -11), ("−", 8)],
        [("+", 14), ("+", -20), ("−", -9)],
        [("+", -18), ("−", 7), ("+", 25)],
        [("+", -3), ("−", -16), ("+", -21)],
        [("+", 32), ("−", 45), ("−", -21)],
        [("+", -27), ("+", -14), ("−", -50)],
        [("+", 40), ("−", -35), ("+", -90)],
        [("+", -120), ("−", -85), ("−", 60)],
    ]
    four = [
        [("+", -8), ("+", 5), ("−", -12), ("−", 6)],
        [("+", 15), ("−", 22), ("+", -9), ("−", -4)],
        [("+", -11), ("−", -11), ("+", 7), ("−", 19)],
        [("+", 24), ("+", -36), ("−", -18), ("+", -10)],
        [("+", -45), ("−", 30), ("−", -62), ("+", 28)],
        [("+", 100), ("−", -250), ("+", -175), ("−", 225)],
    ]
    for t in three + four:
        r = ex_val(t)
        its.append(mcq_v("<p>Evaluate %s.</p>" % ex_text(t), r, ex_cands(t), ex_rule(t)))
    # brackets: a − (p − q) and (a − b) − (c − d) (4)
    for a, p, q in [(-8, 3, 10), (12, -5, 9), (-20, -14, -6)]:
        inner = p - q
        r = a - inner
        txt = "%s %s (%s)" % (n(a), M, sub(p, q))
        e = ("Work out the brackets first: %s = %s. Then %s = %s = <b>%s</b>."
             % (sub(p, q), n(inner), sub(a, inner), add(a, -inner), n(r)))
        its.append(mcq_v("<p>Evaluate %s.</p>" % txt, r,
                         [a - p - q, a + inner, -r, a - abs(inner)], e))
    a, bb, c, d = -6, 13, 4, -9
    l, rr = a - bb, c - d
    r = l - rr
    txt = "(%s) %s (%s)" % (sub(a, bb), M, sub(c, d))
    e = ("Work out each bracket first: %s = %s and %s = %s. Then %s = %s = <b>%s</b>."
         % (sub(a, bb), n(l), sub(c, d), n(rr), sub(l, rr), add(l, -rr), n(r)))
    its.append(mcq_v("<p>Evaluate %s.</p>" % txt, r, [l + rr, a - bb - c - d, -r, l - (c + d)], e))
    assert len(its) == 20
    return {"title": "Expressions with three or more integers", "items": its}


# ============================================================ set 5: word problems
def set_words(rnd, P):
    its = []

    def mq(q, v, cands, e, fmt=n):
        its.append(mcq_v("<p>" + q + "</p>", v, cands, e, fmt=fmt))

    degs = lambda v: plural(v, "degree")
    mm = lambda v: n(v) + NBSP + "m"
    # --- Thunder Bay temperatures (6)
    mq("At 7 a.m. on a January day in Thunder Bay, the temperature was %s. By 2 p.m. it had risen 15 degrees. "
       "What was the temperature at 2 p.m.?" % deg(-27),
       -12, [-42, 12, -13], "Rising means adding: %s = <b>%s</b>." % (add(-27, 15), deg(-12)), fmt=deg)
    mq("In Thunder Bay, it was %s at 4 p.m. The temperature fell 14 degrees by 11 p.m. "
       "What was the temperature at 11 p.m.?" % deg(-8),
       -22, [6, 22, -21], "Falling means subtracting: %s = %s = <b>%s</b>." % (sub(-8, 14), add(-8, -14), deg(-22)), fmt=deg)
    mq("In Thunder Bay, the temperature was %s at 6 a.m. and %s at 3 p.m. How many degrees did the temperature rise?"
       % (deg(-19), deg(-4)),
       15, [23, 19, 4], "Rise = later temperature " + M + " earlier temperature: %s = %s = <b>15 degrees</b>."
       % (sub(-4, -19), add(-4, 19)), fmt=degs)
    mq("On the same February morning, it was %s in Thunder Bay and %s in Toronto. How many degrees warmer was Toronto?"
       % (deg(-31), deg(-6)),
       25, [37, 31, 6], "Find the difference: %s = %s = <b>25 degrees</b>. Both temperatures are below zero, so the "
       "difference is 31 " % (sub(-6, -31), add(-6, 31)) + M + " 6, not 31 + 6.", fmt=degs)
    mq("In Thunder Bay, the temperature dropped 17 degrees overnight. In the morning it was %s. "
       "What was the temperature the evening before?" % deg(-29),
       -12, [-46, 12, 46], "Work backwards: the evening temperature was 17 degrees warmer. %s = <b>%s</b>." % (add(-29, 17), deg(-12)),
       fmt=deg)
    t = [-24, 11, -7]
    mq("In Thunder Bay, it was %s at 6 a.m. The temperature rose 11 degrees by noon, then fell 7 degrees by 9 p.m. "
       "What was the temperature at 9 p.m.?" % deg(-24),
       -20, [-6, -42, 20, -28], "%s = %s = <b>%s</b>." % (add(*t), add(-13, -7), deg(-20)), fmt=deg)
    # --- golf (4)
    nm, he, his = P.next()
    vs = [-2, 3, -4, 1]
    mq("In golf, a score of %s means 3 strokes under par and +2 means 2 strokes over par. %s’s scores for four rounds were "
       "%s, +3, %s and +1. What is %s total score?" % (n(-3), nm, n(-2), n(-4), his),
       -2, [2, -10, 10, -4], "Positives: 3 + 1 = 4. Negatives: %s + (%s) = %s. %s = <b>%s</b>, or 2 under par."
       % (n(-2), n(-4), n(-6), add(4, -6), n(-2)), fmt=signed)
    nm, he, his = P.next()
    mq("After three rounds of a golf tournament, %s is at %s (6 under par). In the final round %s scores +4. "
       "What is %s final score?" % (nm, n(-6), he, his),
       -2, [-10, 2, 10], "%s = <b>%s</b>, or 2 under par." % (add(-6, 4), n(-2)), fmt=signed)
    a, c = P.next(), P.next()
    mq("On a golf leaderboard, %s is at %s and %s is at +2. A lower score is better. How many strokes ahead is %s?"
       % (a[0], n(-7), c[0], a[0]),
       9, [5, 7, 2], "%s = %s = <b>9 strokes</b>." % (sub(2, -7), add(2, 7)), fmt=lambda v: plural(v, "stroke"))
    nm, he, his = P.next()
    mq("%s was at %s after the first nine holes of a round of golf. %s finished the round at +2. "
       "What was %s score on the last nine holes?" % (nm, n(-3), he.capitalize(), his),
       5, [-1, -5, 1], "Change = end " + M + " start: %s = %s = <b>+5</b>, or 5 over par." % (sub(2, -3), add(2, 3)), fmt=signed)
    # --- bank balances (4)
    nm, he, his = P.next()
    mq("%s has $85 in %s bank account. %s pays $120 for winter boots with %s debit card, and the account goes below zero. "
       "What is the balance now?" % (nm, his, he.capitalize(), his),
       -35, [35, -205, 205], "Spending means subtracting: %s = %s = <b>%s</b>." % (sub(85, 120), add(85, -120), money(-35)),
       fmt=money)
    nm, he, his = P.next()
    mq("%s’s bank balance is %s. %s deposits $160 from a summer job. What is the balance now?" % (nm, money(-45), he.capitalize()),
       115, [-115, -205, 205], "A deposit means adding: %s = <b>$115</b>." % add(-45, 160), fmt=money)
    t = [-1250, 3400, -2700]
    mq("A small business in Sudbury has a balance of %s. It receives a payment of $3400, then pays $2700 in rent. "
       "What is the balance now?" % money(-1250),
       -550, add_cands(*t), "%s = %s = <b>%s</b>." % (add(*t), add(2150, -2700), money(-550)), fmt=money)
    nm, he, his = P.next()
    mq("On March 1, %s’s bank balance was %s. On March 31, it was $415. By how much did the balance go up?" % (nm, money(-230)),
       645, [185, 415, -645], "Change = end " + M + " start: %s = %s = <b>$645</b>." % (sub(415, -230), add(415, 230)), fmt=money)
    # --- elevations and depths (4)
    mq("Mount Logan in Yukon is the highest mountain in Canada at 5959" + NBSP + "m above sea level. The deepest point of "
       "Lake Superior is 223" + NBSP + "m below sea level. What is the difference in elevation?",
       6182, [5736, 5959, 223], "%s = %s = <b>6182" % (sub(5959, -223), add(5959, 223)) + NBSP + "m</b>.", fmt=mm)
    nm, he, his = P.next()
    t = [-18, 7, -12]
    mq("%s is scuba diving in Georgian Bay at %s. %s swims up 7" % (nm, metres(-18), he.capitalize()) + NBSP +
       "m, then down 12" + NBSP + "m. What is %s position now?" % his,
       -23, add_cands(*t), "Up is +, down is %s: %s = %s = <b>%s</b>." % (M, add(*t), add(-11, -12), metres(-23)), fmt=metres)
    mq("A research submarine off the coast of Nova Scotia is at %s. It rises 125" % metres(-310) + NBSP +
       "m. What is its new position?",
       -185, [-435, 185, 435], "Rising means adding: %s = <b>%s</b>." % (add(-310, 125), metres(-185)), fmt=metres)
    mq("A plane is flying at 10" + NBSP + "700" + NBSP + "m above sea level. Far below, a submarine is at %s. "
       "What is the vertical distance between them?" % metres(-350),
       11050, [10350, 10700, 350], "%s = %s = <b>11" % (sub(10700, -350), add(10700, 350)) + NBSP + "050" + NBSP + "m</b>.",
       fmt=mm)
    # --- building levels and hockey (2)
    nm, he, his = P.next()
    mq("In a Toronto condo building, the ground floor is level 0 and the parking levels are %s, %s and %s. "
       "%s takes the elevator from level %s up to level 27. How many levels does %s go up?"
       % (n(-1), n(-2), n(-3), nm, n(-3), he),
       30, [24, 27, 3], "%s = %s = <b>30 levels</b>. Count 3 levels up to 0, then 27 more." % (sub(27, -3), add(27, 3)),
       fmt=lambda v: plural(v, "level"))
    nm, he, his = P.next()
    t = [-3, 2, -4, 1]
    mq("In hockey, a player’s plus-minus shows goals for minus goals against while the player is on the ice. "
       "%s’s plus-minus is %s. In the next three games, it changes by +2, %s and +1. What is it now?" % (nm, n(-3), n(-4)),
       -4, [-10, 4, 2, -2], "%s = %s = <b>%s</b>." % (add(*t), add(3, -7), n(-4)))
    assert len(its) == 20
    return {"title": "Word problems: temperature, golf, money and elevation", "items": its}


# ============================================================ lesson
def body_html():
    f_tiles = tiles_rows_svg(3, 5, pairs=True)
    nl = NL(-3, 4).point(-2).point(3).hop(-2, 3, "+5")
    f_sub = nl.svg("number line from " + M + "3 to 4 with 5 hops to the right from " + M + "2 to 3")
    t = [("+", -7), ("+", 12), ("−", -5)]
    return (
        "<h2>The big idea</h2>"
        "<p>Every subtraction can be written as an addition: <b>subtract an integer by adding its opposite</b>. "
        "Then you only need the rules for adding.</p>"
        "<figure class='sn-fig'>" + f_tiles +
        "<figcaption>" + add(3, -5) + ": 3 zero pairs are worth 0. 2 red tiles are left, so " + add(3, -5) +
        " = " + n(-2) + ".</figcaption></figure>"
        "<h2>Rules for adding</h2>" +
        table(["Signs", "What to do", "Example"], [
            ["Same signs", "Add the sizes. Keep the sign.", add(-36, -48) + " = " + n(-84)],
            ["Different signs", "Subtract the sizes. Use the sign of the number farther from 0.", add(-150, 95) + " = " + n(-55)],
        ]) +
        ex("Example 1", "What is " + add(340, -415) + "?",
           "Different signs: 415 " + M + " 340 = 75. " + n(-415) + " is farther from 0, so the answer is negative.", n(-75)) +
        "<h2>Subtracting: add the opposite</h2>"
        "<p>Keep the first number, change " + M + " to +, and change the sign of the number after it.</p>"
        "<figure class='sn-fig'>" + f_sub +
        "<figcaption>" + sub(-2, -5) + " = " + add(-2, 5) + " = 3. Taking away " + n(-5) +
        " moves right, just like adding 5.</figcaption></figure>" +
        ex("Example 2", "What is " + sub(-38, -52) + "?",
           "Add the opposite: " + add(-38, 52) + ". Different signs: 52 " + M + " 38 = 14, and 52 is farther from 0.", "14") +
        "<h2>Expressions with three or more integers</h2>"
        "<p>Rewrite every subtraction as adding the opposite. Then add the positives, add the negatives, and combine.</p>" +
        ex("Example 3", "Evaluate " + ex_text(t) + ".",
           "Add the opposite: " + ex_opp(t) + ". Positives: 12 + 5 = 17. Negatives: " + n(-7) + ". " + add(17, -7) + " = 10.", "10") +
        ex("Example 4", "In Thunder Bay it was " + deg(-24) + " at 6 a.m. and " + deg(-9) + " at 2 p.m. How much did the temperature rise?",
           "Later " + M + " earlier: " + sub(-9, -24) + " = " + add(-9, 24) + " = 15.", "15 degrees") +
        "<h2>Common mistakes</h2>" +
        table(["Mistake", "What to do instead"], [
            [sub(12, -5) + " = 7", "Subtracting a negative is adding: " + add(12, 5) + " = 17"],
            [add(-7, -5) + " = 12", "Same signs keep the sign: " + n(-12)],
            [add(-36, 20) + " = " + n(-56), "Different signs: subtract the sizes. " + add(-36, 20) + " = " + n(-16)],
            [sub(-6, -31) + " = 37", "Add the opposite: " + add(-6, 31) + " = 25"],
            [n(-8) + " " + M + " (3 " + M + " 10) = " + n(-21), "Do the brackets first: " + sub(-8, -7) + " = " + n(-1)],
        ])
    )


FAQ = [
    {"q": "How do you add and subtract integers in Grade 8 math?",
     "a": "Rewrite every subtraction as adding the opposite, then add. With the same signs, add the sizes and keep the sign; with different signs, subtract the sizes and use the sign of the number farther from 0."},
    {"q": "Why is subtracting a negative number the same as adding?",
     "a": "Subtracting means adding the opposite, and the opposite of −5 is 5, so 12 − (−5) = 12 + 5 = 17. On a number line, 12 is 17 steps to the right of −5."},
    {"q": "How do you evaluate an expression like −7 + 12 − (−5)?",
     "a": "Change the subtraction to adding the opposite: −7 + 12 + 5. Add the positives (17) and the negatives (−7), so the answer is 10."},
    {"q": "Do Grade 8 students in Ontario write EQAO?",
     "a": "No. EQAO assessments are written in Grades 3 and 6, and the next math assessment is in Grade 9. Fast, accurate work with integers is used all through Grade 9 math."},
]


def gen():
    rnd = random.Random(48804)
    P = People(rnd)
    sets = [set_review(rnd, P), set_adding(rnd, P), set_subtracting(rnd, P), set_multi(rnd, P), set_words(rnd, P)]
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
        "country": "ca-on", "subject": "math", "grade": "grade-8", "slug": "adding-and-subtracting-integers", "sort": 4,
        "updated": UPDATED, "pdf_url": "",
        "title": "Grade 8 Adding and Subtracting Integers",
        "seo_title": "Grade 8 Adding and Subtracting Integers Worksheets: Free Math Practice with Answer Key (Ontario Curriculum)",
        "short_title": "Adding and subtracting integers",
        "domain": "Number",
        "standard_code": "Grade 8: B2.4",
        "standard_url": "https://www.dcp.edu.gov.on.ca/en/curriculum/elementary-mathematics",
        "standard_text": "Add and subtract integers, using appropriate strategies, in various contexts",
        "meta_desc": "Free Grade 8 math worksheets on adding and subtracting integers for the Ontario curriculum: number lines and zero pairs, sums with larger values, subtracting by adding the opposite, expressions like −7 + 12 − (−5), and word problems with Thunder Bay temperatures, golf scores, bank balances and elevations. 100 questions with an answer key.",
        "key_big": "To subtract an integer, add its opposite: 12 − (−5) = 12 + 5 = 17.",
        "key_sub": "Same signs: add and keep the sign, so −36 + (−48) = −84. Different signs: subtract and use the sign of the number farther from 0. In a longer expression, add the positives, add the negatives, then combine.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }
    return mark_large(u, "(number line|integer tiles)")


if __name__ == "__main__":
    u = gen()
    for st in u["sets"]:          # question text plain like other units
        for it in st["items"]:
            it["q"] = it["q"].replace("<p>", "").replace("</p>", "")
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
