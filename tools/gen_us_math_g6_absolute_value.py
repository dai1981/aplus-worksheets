# -*- coding: utf-8 -*-
"""
US Grade 6 Math: Absolute Value and Ordering Rational Numbers (6.NS.C.7a-d)
  python tools/gen_us_math_g6_absolute_value.py
HTML attributes use single quotes (no backslashes in the JSON).

Numbers are written as strings like "-7", "-1.5", "-3/4", "-1 1/4" and shown with the real
minus sign (U+2212). Every comparison, order and absolute value is checked with Fraction.
Number lines are drawn exactly: each point sits on its value, integers are labeled below the
line and point labels above it never overlap (checked in nl_svg).
Wrong answers come from real mistakes: thinking -7 > -3 because 7 > 3, |-8| = -8, ordering by
absolute value instead of value, ordering negatives as if they were positive, reversing < and >,
counting tick marks instead of spaces, measuring to the opposite instead of to 0.
No integer addition or subtraction (Grade 7).
"""
import json, os, random, re
from fractions import Fraction

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "us", "math", "grade-6")
UPDATED = "2026-11-02"
GREEN = "#006633"
RED = "#c0392b"
INK = "#2b2b2b"
FONT = "Arial, Helvetica, sans-serif"
M = "−"   # real minus sign
GIRLS = ["Maya", "Ava", "Mia", "Zoe", "Lily", "Emma", "Nora", "Ruby", "Sofia", "Grace"]
BOYS = ["Leo", "Noah", "Eli", "Sam", "Ben", "Omar", "Kai", "Jack", "Luis", "Owen"]
LT, GT = "&lt;", "&gt;"


# ------------------------------------------------------------ numbers
def fr(a, b):
    return "<span class='fr'><span class='fn'>%s</span><span class='fd'>%d</span></span>" % (a, b)


class Nm:
    """A rational number from a string like '-7', '-1.5', '-3/4', '-1 1/4'."""

    def __init__(self, s):
        self.s = s
        self.neg = s.startswith("-")
        b = s.lstrip("-")
        self.b = b
        if " " in b:
            w, f = b.split(" ")
            n, d = f.split("/")
            self.kind = "mixed"
            self.parts = (int(w), int(n), int(d))
            v = int(w) + Fraction(int(n), int(d))
        elif "/" in b:
            n, d = b.split("/")
            self.kind = "frac"
            self.parts = (0, int(n), int(d))
            v = Fraction(int(n), int(d))
        else:
            self.kind = "dec" if "." in b else "int"
            v = Fraction(b)
        self.v = -v if self.neg else v
        self.a = v                       # absolute value

    def body(self):
        if self.kind == "frac":
            return fr(self.parts[1], self.parts[2])
        if self.kind == "mixed":
            return "%d %s" % (self.parts[0], fr(self.parts[1], self.parts[2]))
        return self.b

    @property
    def h(self):
        return (M if self.neg else "") + self.body()

    @property
    def ah(self):
        """html of the absolute value."""
        return self.body()

    @property
    def bars(self):
        return "|" + self.h + "|"

    @property
    def plain(self):
        return (M if self.neg else "") + self.b

    def dec(self):
        """Decimal form for fractions, e.g. −0.75 (None for whole numbers and decimals)."""
        if self.kind not in ("frac", "mixed"):
            return None
        x = float(self.v)
        s = ("%.2f" % abs(x)).rstrip("0").rstrip(".")
        return (M if x < 0 else "") + s


def N(*ss):
    return [Nm(s) for s in ss]


def plus_one(x):
    """|x| + 1 as html (counting tick marks instead of spaces)."""
    v = x.a + 1
    if x.kind == "int":
        return str(v)
    if x.kind == "dec":
        return ("%.2f" % float(v)).rstrip("0").rstrip(".")
    w, n, d = x.parts
    return "%d %s" % (w + 1, fr(n, d))


def twice(x):
    v = x.a * 2
    if v.denominator == 1:
        return str(v.numerator)
    if x.kind == "dec":
        return ("%.2f" % float(v)).rstrip("0").rstrip(".")
    w, r = divmod(v.numerator, v.denominator)
    return ("%d %s" % (w, fr(r, v.denominator))) if w else fr(r, v.denominator)


def sym(a, b):
    return LT if a.v < b.v else (GT if a.v > b.v else "=")


def asym(a, b):
    return LT if a.a < b.a else (GT if a.a > b.a else "=")


def cmp_s(a, b, s):
    return "%s %s %s" % (a.h, s, b.h)


def ord_s(xs, sep=", "):
    return sep.join(x.h for x in xs)


def conv_note(xs):
    """'(−3/4 = −0.75)' notes for fractions in a list that also has decimals or other denominators."""
    fs = [x for x in xs if x.dec()]
    if not fs:
        return ""
    if len({x.parts[2] for x in fs}) == 1 and not any(x.kind == "dec" for x in xs):
        return ""
    return " Write the fractions as decimals: " + ", ".join("%s = %s" % (x.h, x.dec()) for x in fs) + "."


# ------------------------------------------------------------ question helpers
def mcq(q, correct, cands, e, rnd):
    seen = {correct}
    pick = []
    for c in cands:
        if c is None or c in seen or not c:
            continue
        seen.add(c)
        pick.append(c)
        if len(pick) == 3:
            break
    assert len(pick) == 3, (q, correct, cands)
    ch = pick + [correct]
    rnd.shuffle(ch)
    return {"q": q, "c": ch, "a": ch.index(correct), "e": e}


def fig(svg):
    return "<div class='qfig'>" + svg + "</div>"


def svg_wrap(w, h, body, label):
    return ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 %d %d' width='%d' height='%d' "
            "role='img' aria-label='%s'><g font-family='%s'>%s</g></svg>" % (w, h, w, h, label, FONT, body))


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


def balance(sets, rnd):
    """Move the correct choice so each position (A to D) is the answer 5 times in every set."""
    for st in sets:
        pos = [0, 1, 2, 3] * 5
        rnd.shuffle(pos)
        for it, t in zip(st["items"], pos):
            ch = it["c"]
            ch[it["a"]], ch[t] = ch[t], ch[it["a"]]
            it["a"] = t


# ------------------------------------------------------------ number line picture
FS = 15          # integer labels
FL = 16          # point labels
FS2 = 13         # stacked fraction digits


def tw(t, fs):
    return len(t) * fs * 0.6


def svg_label(x, y, n, color):
    """Point label for Nm n centered on x, baseline y. Returns (svg, width, height above baseline)."""
    if n.kind in ("int", "dec"):
        t = n.plain
        return ("<text x='%.1f' y='%.1f' font-size='%d' font-weight='700' fill='%s' text-anchor='middle'>%s</text>"
                % (x, y, FL, color, t), tw(t, FL), FL * 0.75)
    w, a, d = n.parts
    lead = (M if n.neg else "") + (str(w) if w else "")
    lw = tw(lead, FL) if lead else 0
    fw = 0.62 * FS2 * max(len(str(a)), len(str(d))) + 4
    gap = 2 if lead else 0
    width = lw + gap + fw
    x0 = x - width / 2
    s = []
    ym = y - 0.32 * FL
    if lead:
        s.append("<text x='%.1f' y='%.1f' font-size='%d' font-weight='700' fill='%s'>%s</text>" % (x0, y, FL, color, lead))
    xf = x0 + lw + gap + fw / 2
    s.append("<text x='%.1f' y='%.1f' font-size='%d' font-weight='700' fill='%s' text-anchor='middle'>%d</text>"
             % (xf, ym - 2, FS2, color, a))
    s.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='1.4'/>"
             % (xf - fw / 2, ym, xf + fw / 2, ym, color))
    s.append("<text x='%.1f' y='%.1f' font-size='%d' font-weight='700' fill='%s' text-anchor='middle'>%d</text>"
             % (xf, ym + 2 + 0.72 * FS2, FS2, color, d))
    return "".join(s), width, (ym - 2 - 0.72 * FS2) * -1 + y


def nl_svg(points, lo=None, hi=None, arcs=(), label=None):
    """Number line with points (Nm list) and distance brackets arcs=[(Nm from, Nm to, text)]."""
    vals = [p.v for p in points] + [Fraction(0)]
    for a, b, _ in arcs:
        vals += [a.v, b.v]
    if lo is None:
        mv = min(vals)
        lo = min(mv - 1 if mv.denominator == 1 else mv // 1, -1)
    if hi is None:
        hv = max(vals)
        hi = max(hv + 1 if hv.denominator == 1 else -(-hv // 1), 1)
    lo, hi = int(lo), int(hi)
    dens = {p.v.denominator for p in points}
    step = Fraction(1, 4) if 4 in dens else (Fraction(1, 2) if 2 in dens else 1)
    U = {1: 32, Fraction(1, 2): 48, Fraction(1, 4): 72}[step]
    pad = 30
    W = int(2 * pad + U * (hi - lo))
    has_fr = any(p.kind in ("frac", "mixed") for p in points)
    X = lambda v: pad + float(v - lo) * U
    # label levels: a label that would touch the one to its left goes one row higher
    lev = {}
    placed = []
    for p in sorted(points, key=lambda p: p.v):
        w = svg_label(0, 0, p, GREEN)[1]
        k = 0
        while any(l == k and abs(bx - X(p.v)) <= (bw + w) / 2 + 4 for bx, bw, l in placed):
            k += 1
        placed.append((X(p.v), w, k))
        lev[p.s] = k
    nlev = max(lev.values()) if lev else 0
    rowh = 34 if has_fr else 22
    top = (34 if has_fr else 26) + rowh * nlev
    if arcs:
        top += 30
    Y = top + 12
    s = ["<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='2'/>" % (pad - 20, Y, W - pad + 20, Y, INK),
         "<path d='M%d %d l9 -5 l0 10 z M%d %d l-9 -5 l0 10 z' fill='%s'/>" % (pad - 22, Y, W - pad + 22, Y, INK)]
    v = Fraction(lo)
    while v <= hi:
        x = X(v)
        if v.denominator == 1:
            s.append("<line x1='%.1f' y1='%d' x2='%.1f' y2='%d' stroke='%s' stroke-width='1.8'/>" % (x, Y - 7, x, Y + 7, INK))
            t = (M + str(-v.numerator)) if v < 0 else str(v.numerator)
            s.append("<text x='%.1f' y='%d' font-size='%d' fill='%s' text-anchor='middle'%s>%s</text>"
                     % (x, Y + 25, FS, INK, " font-weight='700'" if v == 0 else "", t))
        else:
            s.append("<line x1='%.1f' y1='%d' x2='%.1f' y2='%d' stroke='%s' stroke-width='1.3'/>" % (x, Y - 4, x, Y + 4, INK))
        v += step
    # distance brackets (above the line, above the point labels)
    for a, b, t in arcs:
        x1, x2 = sorted([X(a.v), X(b.v)])
        yb = Y - 36 - rowh * nlev
        s.append("<path d='M%.1f %d L%.1f %d L%.1f %d L%.1f %d' fill='none' stroke='%s' stroke-width='2'/>"
                 % (x1, yb + 7, x1, yb, x2, yb, x2, yb + 7, RED))
        s.append("<text x='%.1f' y='%d' font-size='%d' font-weight='700' fill='%s' text-anchor='middle'>%s</text>"
                 % ((x1 + x2) / 2, yb - 7, FS, RED, t))
        assert tw(t.replace("&lt;", "<"), FS) < W, t
    boxes = []
    for p in sorted(points, key=lambda p: p.v):
        x = X(p.v)
        assert lo <= p.v <= hi
        assert (p.v - lo) % step == 0, (p.s, step)
        s.append("<circle cx='%.1f' cy='%d' r='6' fill='%s'/>" % (x, Y, GREEN))
        k = lev[p.s]
        lab, w, h = svg_label(x, Y - 13 - rowh * k, p, GREEN)
        for bx, bw, bk in boxes:
            assert bk != k or abs(bx - x) > (bw + w) / 2 + 4, ("labels overlap", p.s)
        boxes.append((x, w, k))
        assert x - w / 2 > 0 and x + w / 2 < W
        s.append(lab)
    H = Y + 34
    lab = label or ("number line from %s to %s with points at %s" % (
        (M + str(-lo)) if lo < 0 else lo, hi, ", ".join(p.plain for p in sorted(points, key=lambda p: p.v))))
    return svg_wrap(W, H, "".join(s), lab)


# ============================================================ set 1: compare on a number line
def set_compare(rnd, P):
    # (a, b, variant) with a > b. Variants: 1 true statement, 2 greater+why, 3 less+why, 4 meaning of >
    specs = [
        ("-3", "-7", 2), ("0.5", "-1.5", 1), ("4", "-2", 4), ("-5", "-8", 3), ("0", "-6", 1),
        ("-1", "-9", 3), ("3", "-4", 3), ("-1", "-2.5", 4), ("-1/4", "-3/4", 2), ("-6", "-10", 2),
        ("2", "-5", 4), ("-2", "-4", 3), ("1", "-1", 1), ("-4", "-4.5", 2), ("1/4", "-1/2", 3),
        ("-7", "-8", 4), ("-0.5", "-3.5", 1), ("0", "-9", 1), ("-3/4", "-1 1/4", 4), ("-2", "-6", 4),
    ]
    its = []
    for sa, sb, var in specs:
        a, b = Nm(sa), Nm(sb)
        assert a.v > b.v
        flip = rnd.random() < 0.5
        pts = [a, b] if not flip else [b, a]
        pic = fig(nl_svg(pts))
        why = "%s is to the right of %s on the number line, so %s %s %s." % (a.h, b.h, a.h, GT, b.h)
        if a.neg and b.neg:
            why += " Both are negative: the one farther from 0 (%s) is less." % b.h
        elif b.neg and not a.neg:
            if a.v == 0:
                why += " Every negative number is less than 0."
            else:
                why += " A positive number is always greater than a negative number."
        if var == 1:
            x, y = (a, b) if not flip else (b, a)
            if flip:
                why = why.replace("%s is to the right of %s on the number line, so %s %s %s." % (a.h, b.h, a.h, GT, b.h),
                                  "%s is to the left of %s on the number line, so %s %s %s." % (b.h, a.h, b.h, LT, a.h))
            right = cmp_s(x, y, sym(x, y))
            wrong = [cmp_s(x, y, GT if sym(x, y) == LT else LT), cmp_s(y, x, sym(x, y)), cmp_s(x, y, "=")]
            q = pic + "Compare %s and %s. Which statement is true?" % (x.h, y.h)
            its.append(mcq(q, right, wrong, why, rnd))
        elif var == 2:
            assert b.a > a.a
            q = pic + "Which number is greater, %s or %s? Why?" % (pts[0].h, pts[1].h)
            right = "%s, because it is to the right of %s" % (a.h, b.h)
            wrong = ["%s, because it is farther from 0" % b.h, "%s, because it is to the left of %s" % (b.h, a.h),
                     "%s, because it is to the left of %s" % (a.h, b.h)]
            e = why + (" Being farther from 0 does not make a negative number greater." if b.neg else "")
            its.append(mcq(q, right, wrong, e, rnd))
        elif var == 3:
            assert b.a > a.a
            q = pic + "Which number is less, %s or %s? Why?" % (pts[0].h, pts[1].h)
            right = "%s, because it is to the left of %s" % (b.h, a.h)
            wrong = ["%s, because it is closer to 0" % a.h, "%s, because it is to the left of %s" % (a.h, b.h),
                     "%s, because it is to the right of %s" % (b.h, a.h)]
            e = ("%s is to the left of %s, so %s %s %s." % (b.h, a.h, b.h, LT, a.h) +
                 " Being closer to 0 does not make a number less.")
            its.append(mcq(q, right, wrong, e, rnd))
        else:
            x, y = (a, b) if not flip else (b, a)
            s_ = sym(x, y)
            side, other = ("right", "left") if s_ == GT else ("left", "right")
            q = pic + "The statement %s is true. What does it tell you about the number line?" % cmp_s(x, y, s_)
            right = "%s is to the %s of %s" % (x.h, side, y.h)
            dist = []
            if not x.a > y.a:
                dist.append("%s is farther from 0 than %s" % (x.h, y.h))
            if not x.a < y.a:
                dist.append("%s is closer to 0 than %s" % (x.h, y.h))
            if x.a != y.a:
                dist.append("%s and %s are the same distance from 0" % (x.h, y.h))
            wrong = ["%s is to the %s of %s" % (x.h, other, y.h)] + dist
            e = ("“%s” means %s is %s than %s, so %s is to the <b>%s</b> of %s on the number line."
                 % (cmp_s(x, y, s_), x.h, "greater" if s_ == GT else "less", y.h, x.h, side, y.h))
            its.append(mcq(q, right, wrong, e, rnd))
    return {"title": "Compare numbers on a number line", "items": its}


# ============================================================ set 2: order rational numbers
def order_choices(xs, up):
    """Correct order and mistakes: by absolute value, negatives ordered like positives, reversed."""
    right = sorted(xs, key=lambda x: x.v, reverse=not up)
    by_abs = sorted(xs, key=lambda x: x.a, reverse=not up)
    negs = [x for x in xs if x.neg]
    pos = [x for x in xs if not x.neg]
    like_pos = sorted(negs, key=lambda x: x.a) + sorted(pos, key=lambda x: x.v)
    if not up:
        like_pos = like_pos[::-1]
    rev = right[::-1]
    swap = right[:]
    swap[0], swap[1] = swap[1], swap[0]
    return right, [by_abs, like_pos, rev, swap]


def set_order(rnd, P):
    its = []
    lists = [
        (("-3", "5", "-7", "0", "2"), True), (("4", "-1", "-6", "3"), True),
        (("-2.5", "1", "-4", "-0.5"), True), (("-8", "-3", "-10", "-1", "6"), True),
        (("1/2", "-3/4", "-1/4", "1"), True), (("-1.2", "0.8", "-2", "-0.3"), False),
        (("2.5", "-3.5", "-1", "3"), True), (("-5", "-1/2", "-2", "1/4"), True),
        (("-6.5", "-6", "-7", "5"), False), (("0", "-1", "-3/4", "1/2", "-2"), True),
        (("-15", "-20", "5", "-8", "10"), False), (("3/4", "-1 1/2", "-1", "0.5"), True),
        (("-0.4", "-0.25", "0.3", "-1"), True), (("9", "-11", "-2", "7"), False),
    ]
    picks = [
        (("-2", "-11", "4", "-6"), "least"), (("-0.5", "-5", "0.25", "-2.5"), "least"),
        (("-9", "-3", "-12", "-1"), "greatest"), (("-3/4", "-1/2", "-1", "-1/4"), "least"),
        (("-4.5", "-4", "-5", "-0.5"), "greatest"), (("-8", "1", "-13", "-1"), "least"),
    ]
    order = ["L"] * 14 + ["P"] * 6
    rnd.shuffle(order)
    li = pi = 0
    for kind in order:
        if kind == "L":
            ss, up = lists[li]
            li += 1
            xs = N(*ss)
            assert len({x.a for x in xs}) == len(xs)
            right, wr = order_choices(xs, up)
            way = "least to greatest" if up else "greatest to least"
            q = "Order the numbers from <b>%s</b>.<br>%s" % (way, ord_s(xs, ", &nbsp;"))
            e = ("Picture a number line: numbers to the left are less." + conv_note(xs) +
                 " From %s: <b>%s</b>." % (way, ord_s(right)))
            if sum(1 for x in xs if x.neg) >= 2:
                ng = sorted([x for x in xs if x.neg], key=lambda x: x.v)
                e += " Among the negative numbers, %s is farthest from 0, so it is the least." % ng[0].h
            its.append(mcq(q, ord_s(right), [ord_s(w) for w in wr], e, rnd))
        else:
            ss, which = picks[pi]
            pi += 1
            xs = N(*ss)
            right = (min if which == "least" else max)(xs, key=lambda x: x.v)
            q = "Which number is the <b>%s</b>?<br>%s" % (which, ord_s(xs, ", &nbsp;"))
            srt = sorted(xs, key=lambda x: x.v)
            e = ("On a number line, from left to right: %s." % ord_s(srt) + conv_note(xs) +
                 " The %s number is the one farthest to the <b>%s</b>: <b>%s</b>."
                 % (which, "left" if which == "least" else "right", right.h))
            if which == "least" and right.neg:
                e += " A negative number farther from 0 is less."
            elif which == "greatest" and right.neg:
                e += " The negative number closest to 0 is the greatest."
            its.append(mcq(q, right.h, [x.h for x in xs if x is not right], e, rnd))
    return {"title": "Order rational numbers", "items": its}


# ============================================================ set 3: absolute value
def units(h, v):
    return "%s %s" % (h, "unit" if v == 1 else "units")


def set_abs(rnd, P):
    its = []
    # what is |x|
    for s in ["-8", "15", "-2.5", "-3/4", "-24", "-1 1/2"]:
        x = Nm(s)
        q = "What is %s?" % x.bars
        e = ("Absolute value is the distance from 0. %s is %s %s from 0, so %s = <b>%s</b>. "
             "An absolute value is never negative." % (x.h, x.ah, "unit" if x.a == 1 or x.a < 1 else "units", x.bars, x.ah))
        if not x.neg:
            e = ("%s is positive and is %s units from 0, so %s = <b>%s</b>. "
                 "The absolute value of a positive number is the number itself." % (x.h, x.ah, x.bars, x.ah))
        cands = [x.h if x.neg else M + x.body(), "0", plus_one(x), twice(x)]
        its.append(mcq(q, x.ah, cands, e, rnd))
    # distance from 0 with a picture
    for s in ["-6", "9", "-3.5", "-7"]:
        x = Nm(s)
        z = Nm("0")
        pic = fig(nl_svg([x], arcs=[(z, x, "?")]))
        q = pic + "How far is %s from 0 on the number line?" % x.h
        right = units(x.ah, x.a)
        e = ("Count the spaces from 0 to %s, not the tick marks: %s. "
             "Distance is never negative, so %s = <b>%s</b>." % (x.h, units(x.ah, x.a), x.bars, x.ah))
        cands = [units(x.h if x.neg else M + x.body(), 2), units(twice(x), 2), units(plus_one(x), 2), "0 units"]
        its.append(mcq(q, right, cands, e, rnd))
    # which numbers have absolute value n
    for s in ["5", "2.5", "3/4"]:
        x = Nm(s)
        o = Nm("-" + s)
        q = "Which numbers have an absolute value of %s?" % x.h
        right = "%s and %s" % (x.h, o.h)
        cands = ["%s only" % x.h, "%s only" % o.h, "0 and %s" % x.h]
        e = ("Both %s and %s are %s %s from 0, so |%s| = %s and |%s| = %s."
             % (x.h, o.h, x.h, "unit" if x.a <= 1 else "units", x.h, x.h, o.h, x.h))
        its.append(mcq(q, right, cands, e, rnd))
    # greatest / least absolute value
    for ss, which in [(("-9", "7", "-3", "8"), "greatest"), (("-0.5", "2", "-1.5", "1"), "least"),
                      (("4", "-12", "10", "-6"), "greatest"), (("-1/4", "1/2", "-1", "3/4"), "least")]:
        xs = N(*ss)
        assert len({x.a for x in xs}) == 4
        right = (max if which == "greatest" else min)(xs, key=lambda x: x.a)
        q = "Which number has the <b>%s</b> absolute value?<br>%s" % (which, ord_s(xs, ", &nbsp;"))
        e = ("Find each distance from 0: " + ", ".join("%s = %s" % (x.bars, x.ah) for x in xs) +
             ". The %s is %s, so the answer is <b>%s</b>." % (which, right.ah, right.h))
        if which == "greatest":
            e += " The greatest absolute value is the number farthest from 0, not the greatest number."
        else:
            e += " The least absolute value is the number closest to 0, not the least number."
        its.append(mcq(q, right.h, [x.h for x in xs if x is not right], e, rnd))
    # compare absolute values
    for sa, sb in [("-4", "3"), ("-7", "7"), ("-2.5", "-6")]:
        a, b = Nm(sa), Nm(sb)
        s_ = asym(a, b)
        A, B = a.bars, b.bars
        right = "%s %s %s" % (A, s_, B)
        if s_ == "=":
            cands = ["%s %s %s" % (A, LT, B), "%s %s %s" % (A, GT, B), "%s = %s" % (A, a.h)]
        else:
            other = GT if s_ == LT else LT
            cands = ["%s %s %s" % (A, other, B), "%s %s %s" % (B, s_, A), "%s = %s" % (A, a.h)]
        q = "Compare %s and %s. Which statement is true?" % (A, B)
        e = "%s = %s and %s = %s. %s %s %s, so <b>%s</b>." % (A, a.ah, B, b.ah, a.ah, s_, b.ah, right)
        if s_ == "=":
            e = ("%s = %s and %s = %s. Opposites are the same distance from 0, so <b>%s</b>."
                 % (A, a.ah, B, b.ah, right))
        its.append(mcq(q, right, cands, e, rnd))
    # keep the easy |x| questions first, mix the rest
    first = its[:6]
    rest = its[6:]
    rnd.shuffle(rest)
    return {"title": "Absolute value", "items": first[:3] + rest[:5] + first[3:] + rest[5:]}


# ============================================================ set 4: absolute value vs order
def set_vs(rnd, P):
    its = []
    # two-part statements
    for sa, sb in [("-12", "-5"), ("-3", "-8"), ("-9", "4"), ("6", "-10"), ("-1.5", "-0.5"), ("-3", "8")]:
        a, b = Nm(sa), Nm(sb)
        o, ab = sym(a, b), asym(a, b)
        assert o != "=" and ab != "="
        flip = {LT: GT, GT: LT}
        right = "%s %s %s and %s %s %s" % (a.h, o, b.h, a.bars, ab, b.bars)
        cands = ["%s %s %s and %s %s %s" % (a.h, x, b.h, a.bars, y, b.bars)
                 for x, y in [(flip[o], ab), (o, flip[ab]), (flip[o], flip[ab])]]
        q = "Compare %s and %s. Which statement is true?" % (a.h, b.h)
        e = ("Order: %s is to the %s of %s, so %s %s %s. Absolute value: %s = %s and %s = %s, so %s %s %s."
             % (a.h, "left" if o == LT else "right", b.h, a.h, o, b.h, a.bars, a.ah, b.bars, b.ah, a.bars, ab, b.bars))
        if o == LT and ab == GT or o == GT and ab == LT:
            e += " The order and the absolute values do not point the same way."
        its.append(mcq(q, right, cands, e, rnd))
    # is the student right?
    n, he, his = P.next()
    a, b = Nm("-10"), Nm("-2")
    q = "%s says %s %s %s because 10 %s 2. Is %s right?" % (n, a.h, GT, b.h, GT, he)
    right = "No. %s is to the left of %s, so %s %s %s." % (a.h, b.h, a.h, LT, b.h)
    its.append(mcq(q, right, ["Yes. 10 is greater than 2.", "Yes. %s is farther from 0." % a.h,
                              "No. %s = %s because both are negative." % (a.h, b.h)],
                   "10 %s 2 compares the absolute values: |%s| %s |%s|. For the numbers themselves, %s is to the left of %s, so <b>%s %s %s</b>."
                   % (GT, a.h, GT, b.h, a.h, b.h, a.h, LT, b.h), rnd))
    n, he, his = P.next()
    a, b = Nm("-9"), Nm("4")
    q = "%s says %s %s %s because %s %s %s. Is %s right?" % (n, a.bars, LT, b.bars, a.h, LT, b.h, he)
    right = "No. %s = 9 and %s = 4, so %s %s %s." % (a.bars, b.bars, a.bars, GT, b.bars)
    its.append(mcq(q, right, ["Yes. %s is less than %s." % (a.h, b.h), "Yes. %s is to the left of %s." % (a.h, b.h),
                              "No. %s = %s." % (a.bars, b.bars)],
                   "%s %s %s is about order. Absolute value is distance from 0: %s = 9 and %s = 4, so <b>%s %s %s</b>."
                   % (a.h, LT, b.h, a.bars, b.bars, a.bars, GT, b.bars), rnd))
    n, he, his = P.next()
    xs = N("-1", "-4", "-6", "2")
    q = ("%s ordered these numbers from least to greatest: %s. Is %s right?" % (n, ord_s(xs), he))
    srt = sorted(xs, key=lambda x: x.v)
    right = "No. The order is %s." % ord_s(srt)
    its.append(mcq(q, right, ["Yes. 1 %s 4 %s 6, so %s is least." % (LT, LT, xs[0].h),
                              "No. The order is %s." % ord_s(sorted(xs, key=lambda x: x.a)),
                              "No. The order is %s." % ord_s(srt[::-1])],
                   "%s put the negative numbers in order as if they were positive. %s is farthest left, so it is the least: <b>%s</b>."
                   % (n, srt[0].h, ord_s(srt)), rnd))
    n, he, his = P.next()
    q = ("%s says the number with the greater absolute value is always the greater number. Is %s right?" % (n, he))
    a, b = Nm("-8"), Nm("3")
    right = "No. %s %s %s, but %s %s %s." % (a.bars, GT, b.bars, a.h, LT, b.h)
    its.append(mcq(q, right, ["Yes. %s %s %s, so %s %s %s." % (a.bars, GT, b.bars, a.h, GT, b.h),
                              "Yes. It is true for every number.",
                              "No. %s %s %s, but %s %s %s." % (a.bars, LT, b.bars, a.h, LT, b.h)],
                   "It is not true for negative numbers. %s is farther from 0 than %s, so %s %s %s. "
                   "But %s is to the left of %s, so <b>%s %s %s</b>." % (a.h, b.h, a.bars, GT, b.bars, a.h, b.h, a.h, LT, b.h), rnd))
    # find a number that fits two conditions
    finds = [
        ("greater than %s but has a greater absolute value than %s", "-6", ["8", "-8", "5", "-5"],
         lambda x, t: x.v > t.v and x.a > t.a),
        ("less than %s but has a greater absolute value than %s", "3", ["-4", "4", "2", "-2"],
         lambda x, t: x.v < t.v and x.a > t.a),
        ("less than %s but has an absolute value less than 9", "-5", ["-7", "-11", "-3", "7"],
         lambda x, t: x.v < t.v and x.a < 9),
        ("greater than %s but has a greater absolute value than %s", "-1", ["2", "-2", "0", "-1/2"],
         lambda x, t: x.v > t.v and x.a > t.a),
    ]
    for tpl, ts, cs, ok in finds:
        t = Nm(ts)
        xs = N(*cs)
        good = [x for x in xs if ok(x, t)]
        assert len(good) == 1, (tpl, cs)
        g = good[0]
        cond = tpl.replace("%s", t.h)
        q = "Which number is %s?" % cond
        parts = []
        for x in xs:
            c1 = "%s %s %s" % (x.h, sym(x, t), t.h)
            parts.append("%s: %s, |%s| = %s" % (x.h, c1, x.h, x.ah))
        e = "Check both parts for each number. " + "; ".join(parts) + ". Only <b>%s</b> fits both." % g.h
        its.append(mcq(q, g.h, [x.h for x in xs if x is not g], e, rnd))
    # order by absolute value
    for ss in [("-7", "3", "-1", "5"), ("2", "-6", "-4.5", "1"), ("-1/2", "-3", "1/4", "2")]:
        xs = N(*ss)
        right = sorted(xs, key=lambda x: x.a)
        q = "Order the numbers from <b>least to greatest absolute value</b>.<br>%s" % ord_s(xs, ", &nbsp;")
        byv = sorted(xs, key=lambda x: x.v)
        cands = [ord_s(byv), ord_s(right[::-1]), ord_s(byv[::-1])]
        e = ("Find each absolute value: " + ", ".join("%s = %s" % (x.bars, x.ah) for x in xs) +
             ". Closest to 0 comes first: <b>%s</b>. This is not the same as ordering the numbers (%s)." % (ord_s(right), ord_s(byv)))
        its.append(mcq(q, ord_s(right), cands, e, rnd))
    # which statement is false
    for sa, sb in [("-12", "-5"), ("-4", "-9"), ("-7", "2")]:
        a, b = Nm(sa), Nm(sb)
        o, ab = sym(a, b), asym(a, b)
        side = "left" if o == LT else "right"
        trues = [cmp_s(a, b, o), "%s %s %s" % (a.bars, ab, b.bars), "%s is to the %s of %s" % (a.h, side, b.h)]
        false = cmp_s(a, b, GT if o == LT else LT)
        q = "Look at %s and %s. Which statement is <b>false</b>?" % (a.h, b.h)
        e = ("%s is to the %s of %s, so %s %s %s, not %s. The other statements are true: %s = %s and %s = %s, so %s %s %s."
             % (a.h, side, b.h, a.h, o, b.h, false, a.bars, a.ah, b.bars, b.ah, a.bars, ab, b.bars))
        its.append(mcq(q, false, trues, e, rnd))
    rnd.shuffle(its)
    return {"title": "Absolute value vs. order", "items": its}


# ============================================================ set 5: word problems
def money(s):
    return (M if s.startswith("-") else "") + "$" + s.lstrip("-")


def deg(s, u="F"):
    return "%s °%s" % ((M if s.startswith("-") else "") + s.lstrip("-"), u)


def ft(s):
    return "%s feet" % ((M if s.startswith("-") else "") + s.lstrip("-"))


def set_words(rnd, P):
    its = []

    def add(q, right, cands, e):
        its.append(mcq(q, right, cands, e, rnd))

    # 1 temperatures in two cities
    add("At 7 a.m., it was %s in Fargo and %s in Omaha. Which statement is true?" % (deg("-4"), deg("2")),
        "%s %s %s, so Fargo was colder." % (deg("-4"), LT, deg("2")),
        ["%s %s %s, so Fargo was warmer." % (deg("-4"), GT, deg("2")),
         "%s %s %s, so Fargo was colder." % (deg("-4"), GT, deg("2")),
         "%s %s %s, so Omaha was colder." % (deg("-4"), LT, deg("2"))],
        "%s is to the left of %s on a thermometer number line, so %s %s %s. The lower temperature is colder: <b>Fargo was colder</b>."
        % (M + "4", "2", M + "4", LT, "2"))
    # 2 coldest day
    days = [("Monday", "-3"), ("Tuesday", "-8"), ("Wednesday", "1"), ("Thursday", "-5")]
    add("The low temperatures for four days were: Monday %s, Tuesday %s, Wednesday %s, Thursday %s. Which day was the coldest?"
        % tuple(deg(t, "C") for _, t in days),
        "Tuesday", ["Monday", "Wednesday", "Thursday"],
        "The coldest day has the least temperature. From least to greatest: %s. %s is the least, so <b>Tuesday</b> was the coldest."
        % (", ".join(deg(t, "C") for t in ["-8", "-5", "-3", "1"]), deg("-8", "C")))
    # 3 freezer
    add("A freezer must stay colder than %s. Which temperature is colder than %s?" % (deg("-5"), deg("-5")),
        deg("-7"), [deg("-3"), deg("0"), deg("5")],
        "Colder means less. %s %s %s, because %s is to the left of %s. So <b>%s</b> is colder. (%s %s %s, so %s is warmer.)"
        % (M + "7", LT, M + "5", M + "7", M + "5", deg("-7"), M + "3", GT, M + "5", deg("-3")))
    # 4 who owes more
    (n1, _, _), (n2, _, _) = P.next(), P.next()
    add("%s’s bank account balance is %s. %s’s balance is %s. Who owes more money?" % (n1, money("-30"), n2, money("-20")),
        "%s, because %s is a debt of $30" % (n1, money("-30")),
        ["%s, because %s %s %s" % (n2, money("-20"), GT, money("-30")),
         "%s, because %s is a debt of $20" % (n2, money("-20")),
         "They owe the same amount"],
        "A negative balance is a debt. |%s| = 30, so %s owes $30. |%s| = 20, so %s owes $20. "
        "<b>%s</b> owes more, even though %s %s %s." % (M + "30", n1, M + "20", n2, n1, money("-30"), LT, money("-20")))
    # 5 debt more than 25
    add("Which account balance shows a debt of <b>more</b> than $25?",
        money("-30"), [money("-20"), money("30"), money("-25")],
        "A balance of %s is a debt of $30, and 30 %s 25. %s is a debt of $20, %s is a debt of exactly $25, and $30 is not a debt. "
        "A balance less than %s means a debt greater than $25." % (money("-30"), GT, money("-20"), money("-25"), money("-25")))
    # 6 how much owed
    n, he, his = P.next()
    add("%s’s account balance is %s. How much money does %s owe?" % (n, money("-45"), he),
        "$45", [money("-45"), "$0", "%s does not owe money" % cap(he)],
        "A negative balance is a debt. The size of the debt is the absolute value: |%s| = 45. %s owes <b>$45</b>."
        % (M + "45", cap(he)))
    # 7 order balances
    bs = N("15", "-40", "-10", "0")
    srt = sorted(bs, key=lambda x: x.v)
    fm = lambda xs: ", ".join(money(x.s) for x in xs)
    add("Four friends have these account balances: %s. Order the balances from least to greatest." % fm(bs),
        fm(srt), [fm(sorted(bs, key=lambda x: x.a)), fm([bs[2], bs[1], bs[3], bs[0]]), fm(srt[::-1])],
        "The biggest debt is the least balance. From least to greatest: <b>%s</b>. %s %s %s because a debt of $40 is more than a debt of $10."
        % (fm(srt), money("-40"), LT, money("-10")))
    # 8 deeper
    add("A diver is at %s. A submarine is at %s. Which one is deeper?" % (ft("-40"), ft("-120")),
        "The submarine, because %s %s %s" % (M + "120", LT, M + "40"),
        ["The diver, because %s %s %s" % (M + "40", LT, M + "120"),
         "The diver, because 40 %s 120" % LT, "They are at the same depth"],
        "Deeper means lower. %s is to the left of (below) %s, so %s %s %s. <b>The submarine</b> is deeper: 120 feet below sea level."
        % (M + "120", M + "40", M + "120", LT, M + "40"))
    # 9 below sea level
    add("A fish is swimming at an elevation of %s. How far below sea level is it?" % ft("-18"),
        "18 feet", [ft("-18"), "0 feet", "36 feet"],
        "Sea level is 0. The distance from 0 is the absolute value: |%s| = 18. The fish is <b>18 feet</b> below sea level."
        % (M + "18"))
    # 10 farther from sea level
    add("A bird is flying at 25 feet. A fish is swimming at %s. Which one is farther from sea level?" % ft("-30"),
        "The fish, because |%s| %s |25|" % (M + "30", GT),
        ["The bird, because 25 %s %s" % (GT, M + "30"), "They are the same distance from sea level",
         "The bird, because it is above sea level"],
        "Distance from sea level is absolute value. |%s| = 30 and |25| = 25. 30 %s 25, so <b>the fish</b> is farther from sea level, "
        "even though 25 %s %s." % (M + "30", GT, GT, M + "30"))
    # 11 lowest place
    places = [("a beach", "0"), ("a valley", "-86"), ("a hill", "120"), ("a mine tunnel", "-250")]
    add("Four places have these elevations: %s. Which place is the lowest?"
        % "; ".join("%s at %s" % (p, ft(v)) for p, v in places),
        "The mine tunnel", ["The valley", "The beach", "The hill"],
        "The lowest place has the least elevation. %s %s %s %s 0 %s 120, so <b>the mine tunnel</b> is the lowest."
        % (M + "250", LT, M + "86", LT, LT))
    # 12 golf winner
    (g1, _, _), (g2, _, _) = P.next(), P.next()
    add("In golf, the lowest score wins. %s’s score is %s. %s’s score is %s. Who wins?" % (g1, M + "3", g2, M + "1"),
        "%s, because %s %s %s" % (g1, M + "3", LT, M + "1"),
        ["%s, because %s %s %s" % (g2, M + "1", GT, M + "3"),
         "%s, because 1 %s 3" % (g2, LT),
         "%s, because %s %s %s" % (g1, M + "3", GT, M + "1")],
        "%s is to the left of %s, so %s %s %s. The lowest score wins, so <b>%s</b> wins."
        % (M + "3", M + "1", M + "3", LT, M + "1", g1))
    # 13 golf order
    gs = N("-2", "1", "-5", "0")
    srt = sorted(gs, key=lambda x: x.v)
    add("In golf, a lower score is better. Four players scored %s. Order the scores from best to worst." % ord_s(gs),
        ord_s(srt), [ord_s(sorted(gs, key=lambda x: x.a)), ord_s(srt[::-1]), ord_s([gs[0], gs[2], gs[3], gs[1]])],
        "Best to worst means least to greatest: <b>%s</b>. %s is the best score because it is the least." % (ord_s(srt), srt[0].h))
    # 14 noon vs night
    add("At noon, the temperature was %s. At midnight, it was %s. Which statement is true?" % (deg("-6"), deg("-11")),
        "%s %s %s, so it was colder at midnight" % (M + "11", LT, M + "6"),
        ["%s %s %s, so it was colder at midnight" % (M + "11", GT, M + "6"),
         "%s %s %s, so it was colder at noon" % (M + "11", GT, M + "6"),
         "%s %s %s, so it was colder at noon" % (M + "6", LT, M + "11")],
        "%s is farther below 0 than %s, so %s %s %s. The lower temperature is colder: <b>midnight</b>."
        % (deg("-11"), deg("-6"), M + "11", LT, M + "6"))
    # 15 closer to 0
    add("One morning, it was %s in Anchorage and %s in Denver. Which city’s temperature was closer to %s?"
        % (deg("-9"), deg("-2"), deg("0")),
        "Denver", ["Anchorage", "They were the same distance from %s" % deg("0"), "You can’t tell"],
        "Closer to 0 means the smaller absolute value. |%s| = 9 and |%s| = 2. 2 %s 9, so <b>Denver</b> was closer to %s."
        % (M + "9", M + "2", LT, deg("0")))
    # 16 football
    add("In a football game, a team gained 5 yards on one play (+5) and lost 7 yards on the next play (%s). "
        "On which play did the ball move a greater distance?" % (M + "7"),
        "The second play, because |%s| %s |5|" % (M + "7", GT),
        ["The first play, because 5 %s %s" % (GT, M + "7"), "Both plays moved the ball the same distance",
         "The first play, because a gain is always more"],
        "Distance is absolute value: |5| = 5 and |%s| = 7. 7 %s 5, so the ball moved farther on <b>the second play</b>, even though 5 %s %s."
        % (M + "7", GT, GT, M + "7"))
    # 17 most money
    ppl = [P.next()[0] for _ in range(4)]
    bal = ["-12", "3", "-40", "0"]
    add("%s has a balance of %s, %s has %s, %s has %s, and %s has %s. Who has the greatest balance?"
        % (ppl[0], money(bal[0]), ppl[1], money(bal[1]), ppl[2], money(bal[2]), ppl[3], money(bal[3])),
        ppl[1], [ppl[2], ppl[0], ppl[3]],
        "The greatest balance is the one farthest right on a number line: %s %s %s %s $0 %s $3. "
        "<b>%s</b> has the greatest balance, $3. %s has the greatest debt, not the most money."
        % (money("-40"), LT, money("-12"), LT, LT, ppl[1], ppl[2]))
    # 18 decimal thermometers
    add("Thermometer A shows %s. Thermometer B shows %s. Which thermometer shows the colder temperature?"
        % (deg("-2.5", "C"), deg("-1.5", "C")),
        "Thermometer A, because %s %s %s" % (M + "2.5", LT, M + "1.5"),
        ["Thermometer B, because %s %s %s" % (M + "1.5", LT, M + "2.5"),
         "Thermometer B, because 1.5 %s 2.5" % LT,
         "Thermometer A, because %s %s %s" % (M + "2.5", GT, M + "1.5")],
        "%s is to the left of %s, so %s %s %s. The lower temperature is colder: <b>Thermometer A</b>."
        % (M + "2.5", M + "1.5", M + "2.5", LT, M + "1.5"))
    # 19 colder next day
    add("The low temperature on Monday was %s. On Tuesday, the low was even colder. Which could be Tuesday’s low?" % deg("-7"),
        deg("-9"), [deg("-5"), deg("0"), deg("7")],
        "Colder means less than %s, so the number must be to the left of %s. %s %s %s, so <b>%s</b> could be Tuesday’s low. "
        "%s is warmer, because %s %s %s." % (M + "7", M + "7", M + "9", LT, M + "7", deg("-9"), deg("-5"), M + "5", GT, M + "7"))
    # 20 balance less than -50
    n, he, his = P.next()
    add("%s’s account balance is less than %s. What does this tell you about %s debt?" % (n, money("-50"), his),
        "%s owes more than $50" % cap(he),
        ["%s owes less than $50" % cap(he), "%s owes exactly $50" % cap(he), "%s does not owe any money" % cap(he)],
        "A balance less than %s is to the left of %s, like %s. That is farther from 0, so the debt is <b>more than $50</b>."
        % (money("-50"), money("-50"), money("-60")))
    return {"title": "Absolute value and order word problems", "items": its}


# ============================================================ lesson
def body_html():
    a, b = Nm("-7"), Nm("-3")
    p1 = nl_svg([a, b], -8, 2, label="number line from −8 to 2 with points at −7 and −3")
    five, mfive, zero = Nm("5"), Nm("-5"), Nm("0")
    p2 = nl_svg([mfive, five], -6, 6, arcs=[(mfive, zero, "5 units"), (zero, five, "5 units")],
                label="number line: −5 and 5 are both 5 units from 0")
    return (
        "<h2>Order on the number line</h2>"
        "<p>On a number line, numbers get <b>greater</b> as you move to the <b>right</b>. "
        "A number to the left is less. This is true for negative numbers, too.</p>"
        "<figure class='sn-fig'>" + p1 +
        "<figcaption>" + M + "7 is to the left of " + M + "3, so " + M + "7 " + LT + " " + M + "3.</figcaption></figure>"
        "<p>Write the result with a symbol. <b>" + LT + "</b> means “is less than.” <b>" + GT + "</b> means “is greater than.” "
        "The symbol opens toward the greater number.</p>" +
        ex("Example", "Compare " + M + "3 and " + M + "7.",
           M + "3 is to the right of " + M + "7. So " + M + "3 is greater. Both are negative, so the one closer to 0 is greater.",
           M + "3 " + GT + " " + M + "7") +
        ex("Example", "Compare " + M + "1.5 and 0.5.",
           "Every negative number is to the left of 0, and 0.5 is to the right of 0.",
           M + "1.5 " + LT + " 0.5") +
        "<h2>Order a list</h2>"
        "<p>To order numbers from least to greatest, put them in order from left to right on a number line. "
        "Write fractions as decimals when the list mixes them.</p>" +
        ex("Example", "Order from least to greatest: 2, " + M + fr(3, 4) + ", " + M + "1.5, 0.",
           M + fr(3, 4) + " = " + M + "0.75. The negative numbers come first. " + M + "1.5 is farther from 0 than " + M +
           "0.75, so it is less.",
           M + "1.5, " + M + fr(3, 4) + ", 0, 2") +
        "<h2>Absolute value is distance from 0</h2>"
        "<p>The <b>absolute value</b> of a number is its distance from 0. We write it with bars: |" + M + "5| is read “the absolute value of " + M + "5.” "
        "Distance is never negative, so an absolute value is never negative.</p>"
        "<figure class='sn-fig'>" + p2 +
        "<figcaption>|" + M + "5| = 5 and |5| = 5. Opposites have the same absolute value.</figcaption></figure>" +
        table(["Number", "Distance from 0", "Absolute value"], [
            [M + "8", "8 units", "|" + M + "8| = 8"],
            ["8", "8 units", "|8| = 8"],
            [M + "2.5", "2.5 units", "|" + M + "2.5| = 2.5"],
            ["0", "0 units", "|0| = 0"],
        ]) +
        "<h2>Absolute value is not the same as order</h2>"
        "<p>For negative numbers, a greater absolute value means a <b>lesser</b> number. " + M + "12 is farther from 0 than " + M +
        "5, so |" + M + "12| " + GT + " |" + M + "5|. But " + M + "12 is to the left of " + M + "5, so " + M + "12 " + LT + " " + M + "5.</p>" +
        ex("Example", "A balance of " + M + "$30 and a balance of " + M + "$20. Which is the bigger debt?",
           "|" + M + "30| = 30 and |" + M + "20| = 20. The debt is the absolute value. The balance " + M + "$30 is less, but the debt is greater.",
           "a debt of $30 is more than a debt of $20, and " + M + "$30 " + LT + " " + M + "$20") +
        ex("Example", "It is " + M + "4 °F in one town and 2 °F in another. Which town is colder?",
           M + "4 is to the left of 2, so " + M + "4 " + LT + " 2. The lower temperature is colder.",
           "the town at " + M + "4 °F") +
        "<h2>Common mistakes</h2>" +
        table(["Mistake", "What to do instead"], [
            ["Thinking " + M + "7 " + GT + " " + M + "3 because 7 " + GT + " 3", "Look at the number line: " + M + "7 is farther left, so " + M + "7 " + LT + " " + M + "3"],
            ["Writing |" + M + "8| = " + M + "8", "Absolute value is a distance: |" + M + "8| = 8"],
            ["Ordering by absolute value: " + M + "1, 2, " + M + "5", "Order by position: " + M + "5, " + M + "1, 2"],
            ["Mixing up " + LT + " and " + GT, "The symbol opens toward the greater number: " + M + "3 " + GT + " " + M + "7"],
            ["Counting tick marks instead of spaces", "|" + M + "6| is 6 spaces from 0, not 7 marks"],
            ["Thinking the bigger debt is the greater balance", M + "$30 is a bigger debt than " + M + "$20, but " + M + "$30 " + LT + " " + M + "$20"],
        ])
    )


FAQ = [
    {"q": "What is absolute value in 6th grade math?",
     "a": "The absolute value of a number is its distance from 0 on the number line. |−8| = 8 and |8| = 8, and an absolute value is never negative."},
    {"q": "Is −7 greater than −3?",
     "a": "No. −7 is to the left of −3 on the number line, so −7 < −3. A negative number farther from 0 is less."},
    {"q": "How do you order negative numbers from least to greatest?",
     "a": "Put them in order from left to right on a number line. The negative number farthest from 0 comes first, and positive numbers come after 0, for example −5, −1, 0, 2."},
    {"q": "What is the difference between comparing numbers and comparing absolute values?",
     "a": "Comparing numbers asks which is farther right; comparing absolute values asks which is farther from 0. −12 < −5, but |−12| > |−5|, so a balance of −$12 is the bigger debt."},
]


def gen_unit():
    rnd = random.Random(613)
    P = People(rnd)
    sets = [set_compare(rnd, P), set_order(rnd, P), set_abs(rnd, P), set_vs(rnd, P), set_words(rnd, P)]
    seen = set()
    for s in sets:
        assert len(s["items"]) == 20, (s["title"], len(s["items"]))
        for it in s["items"]:
            assert len(set(it["c"])) == 4, it
            assert it["q"] not in seen, it["q"]
            seen.add(it["q"])
    balance(sets, rnd)
    return {
        "country": "us", "subject": "math", "grade": "grade-6", "slug": "absolute-value-and-ordering", "sort": 13,
        "updated": UPDATED, "pdf_url": "",
        "title": "Absolute Value and Ordering Rational Numbers",
        "seo_title": "Grade 6 Absolute Value Worksheets: Compare and Order Rational Numbers on a Number Line",
        "short_title": "Absolute Value and Ordering",
        "domain": "The Number System",
        "standard_code": "6.NS.C.7",
        "standard_url": "https://www.thecorestandards.org/Math/Content/6/NS/C/7/",
        "standard_text": "Understand ordering and absolute value of rational numbers.",
        "meta_desc": "Free Grade 6 absolute value worksheets: compare negative numbers with < and >, order integers, decimals and fractions, find absolute value as distance from 0, and solve temperature, debt and elevation word problems. 100 practice questions with answers.",
        "key_big": "Farther right means greater. Absolute value is the distance from 0.",
        "key_sub": "−7 < −3 because −7 is farther left, but |−7| > |−3| because −7 is farther from 0. An absolute value is never negative.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }


if __name__ == "__main__":
    u = gen_unit()
    mark_large(u, "number line")
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(u, f, ensure_ascii=False, indent=1)
    print("wrote", path)
